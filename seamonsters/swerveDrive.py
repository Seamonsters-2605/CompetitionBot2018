__author__ = "jacobvanthoog"

from drive import DriveInterface
from jeffMode import JeffMode
import drive
import math
import wpilib

def magnitude(vector):
    return math.sqrt(vector[0]**2.0 + vector[1]**2.0)

def direction(vector):
    result = math.atan2(vector[1], vector[0])
    if result < 0:
        result += math.pi * 2
    return result

def normalize(vector):
    mag = magnitude(vector)
    return (vector[0] / mag, vector[1] / mag)

class WheelState:
    # location is a tuple (x, y) -- location of wheel from center of robot
    def __init__(self, location, controller):
        self.location = location
        self.driveVector = (0, 0)
        self.targetDirection = 0
        self.targetMagnitude = 0
        self.invertMagnitude = False
        
        self.controller = controller
    
    def calcDrive(self, mag, driveDirection, turn):
        moveVector = (math.cos(driveDirection) * mag,
                math.sin(driveDirection) * mag)
        self.driveVector = (moveVector[0] - self.location[1]*turn,
                moveVector[1] + self.location[0]*turn)
        self.targetMagnitude = magnitude(self.driveVector)
        self.targetDirection = direction(self.driveVector)
    
    def drive(self, driveMode):
        # set rotate talon
        currentRot = self.controller.getCurrentRotation()
        diffRadians = abs(currentRot - self.targetDirection) % (math.pi*2)
        self.invertMagnitude = diffRadians > math.radians(90) \
                and diffRadians < math.radians(270)
        targetMotorRot = self.targetDirection # in radians
        if self.invertMagnitude:
            targetMotorRot += math.radians(180)
            targetMotorRot %= math.pi*2
        self.controller.rotateWheel(targetMotorRot)
        
        # set drive talon
        self.controller.setDriveMode(driveMode)
        mag = self.targetMagnitude
        if self.invertMagnitude:
            mag = -mag
        self.controller.setSpeed(mag)


# an interface for controlling a single swerve drive wheel
class WheelController:
    
    # orient the wheel towards a certain direction
    # radians may not be within 0 and 2pi
    def rotateWheel(self, radians):
        pass
    
    # in radians
    def getCurrentRotation(self):
        pass
    
    # spin the wheel
    def setSpeed(self, speed):
        pass
    
    def setDriveMode(self, driveMode):
        pass


class TestWheelController(WheelController):
    
    def __init__(self):
        self.rotation = 0
        
    def rotateWheel(self, radians):
        print("Rotating wheel to", math.degrees(radians))
        self.rotation = radians
        
    def setSpeed(self, speed):
        print("Wheel speed set to", speed)
        
    def getCurrentRotation(self):
        return self.rotation
    
    def setDriveMode(self, driveMode):
        print("Set drive mode to", driveMode)


class TalonWheelController(WheelController):
    
    def __init__(self, driveTalon, rotateTalon, rotateTalonEncoderTicks):
        self.driveTalon = driveTalon
        self.driveTalonJeff = JeffMode(self.driveTalon)
        
        self.rotateTalon = rotateTalon
        self.rotateTalonInitialPosition = rotateTalon.getPosition()
        self.rotateTalonEncoderTicks = rotateTalonEncoderTicks
        rotateTalon.changeControlMode(wpilib.CANTalon.ControlMode.Position)

    def getCurrentRotation(self):
        ticks = self.rotateTalon.getPosition()
        ticks %= self.rotateTalonEncoderTicks
        ticks -= self.rotateTalonInitialPosition
        return float(ticks) / float(self.rotateTalonEncoderTicks) * math.pi * 2
        
    def rotateWheel(self, target):
        targetTicks = target / (math.pi * 2) * self.rotateTalonEncoderTicks \
            + self.rotateTalonInitialPosition
        currentTicks = self.rotateTalon.getPosition()
        diff = targetTicks - currentTicks
        diff %= self.rotateTalonEncoderTicks
        self.rotateTalon.set(currentTicks + diff)
    
    def setDriveMode(self, driveMode):
        seamonsters.drive.setControlMode(self.driveTalon, driveMode)
        
    def setSpeed(self, speed):
        pass


class SwerveDrive(DriveInterface):
    
    def __init__(self):
        DriveInterface.__init__(self)
        self.wheels = [ ]
    
    def addWheel(self, location):
        self.wheels.append(WheelState(location, TestWheelController()))
    
    def drive(self, magnitude, direction, turn, forceDriveMode = None):
        if forceDriveMode == None:
            forceDriveMode = self.getDriveMode()
        for wheel in self.wheels:
            wheel.calcDrive(magnitude, direction, turn)
            wheel.drive(forceDriveMode)
    
    def printWheelState(self):
        for i, wheel in enumerate(self.wheels):
            print("Wheel:", i,
                  "Vector:", wheel.driveVector,
                  "Magnitude:", wheel.targetMagnitude,
                  "Direction:", math.degrees(wheel.targetDirection))


def test_swervedrive_forward():
    
    drive = SwerveDrive()
    drive.addWheel((1.0,1.0))
    drive.addWheel((-1.0,1.0))
    drive.addWheel((1.0,-1.0))
    drive.addWheel((-1.0,-1.0))
    drive.drive(4, math.radians(90), 0)
    assert drive.wheels[1].targetMagnitude == 4