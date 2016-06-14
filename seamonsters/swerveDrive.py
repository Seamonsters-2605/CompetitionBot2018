__author__ = "jacobvanthoog"

from seamonsters.drive import DriveInterface
import seamonsters.drive
from seamonsters.jeffMode import JeffMode
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
    """
    Keeps track of the current state of a single wheels, calculates all the
    necessary, vector math, and controls a WheelController.
    """
    
    def __init__(self, location, controller):
        """
        location is a tuple (x, y) -- location of wheel from center of robot.
        controller is a WheelController.
        """
        self.location = location
        self.driveVector = (0, 0)
        self.targetDirection = 0
        self.targetMagnitude = 0
        self.invertMagnitude = False
        
        self.controller = controller
    
    def calcDrive(self, mag, driveDirection, turn):
        """
        Calculate the drive vector, magnitude, and direction for the given
        parameters, but don't do anything yet.
        """
        moveVector = (math.cos(driveDirection) * mag,
                math.sin(driveDirection) * mag)
        self.driveVector = (moveVector[0] - self.location[1]*turn,
                moveVector[1] + self.location[0]*turn)
        self.targetMagnitude = magnitude(self.driveVector)
        # don't rotate wheel if not driving
        if self.targetMagnitude != 0:
            self.targetDirection = direction(self.driveVector)
    
    def drive(self, driveMode, scale):
        """
        Use the WheelController to drive with previously calculated values.
        scale multiplies all driving motor values by a constant -- different
        drive mode max velocities have already been included in this.
        """
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
        self.controller.setSpeed(mag * scale)


class WheelController:
    """
    An interface for controlling a single swerve drive wheel
    """
    
    def rotateWheel(self, radians):
        """
        Orient the wheel towards a certain direction.
        radians might not be within 0 and 2pi
        """
        pass
    
    def getCurrentRotation(self):
        """
        Get the current orientation of the wheel, in radians.
        """
        pass
    
    def setSpeed(self, speed):
        """
        Spin the wheel at the specific speed. The speed has already been
        adjusted for the current drive mode.
        """
        pass
    
    def setDriveMode(self, driveMode):
        """
        Set the drive mode for the driving motor (not for the rotation motor).
        """
        pass


class TestWheelController(WheelController):
    """
    A wheel controller that logs all events and does nothing else.
    """
    
    def __init__(self, number):
        self.number = number
        self.rotation = 0
        
    def rotateWheel(self, radians):
        print("Wheel", self.number, "rotating to", math.degrees(radians))
        self.rotation = radians
        
    def setSpeed(self, speed):
        print("Wheel", self.number, "speed set to", speed)
        
    def getCurrentRotation(self):
        return self.rotation
    
    def setDriveMode(self, driveMode):
        print("Wheel", self.number, "drive mode set to", driveMode)


class TalonWheelController(WheelController):
    """
    A wheel controller controlling two CANTalons. Supports any drive mode.
    """
    
    def __init__(self, driveTalon, rotateTalon, rotateTalonEncoderTicks):
        self.driveTalon = driveTalon
        self.driveTalonJeff = JeffMode(self.driveTalon)
        
        self.rotateTalon = rotateTalon
        self.rotateTalonInitialPosition = rotateTalon.getPosition()
        self.rotateTalonEncoderTicks = abs(rotateTalonEncoderTicks)
        self.reverseRotateTalon = rotateTalonEncoderTicks < 0
        rotateTalon.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        
        self.driveMode = DriveInterface.DriveMode.VOLTAGE

    def getCurrentRotation(self):
        ticks = self.rotateTalon.getPosition()
        ticks %= self.rotateTalonEncoderTicks
        ticks -= self.rotateTalonInitialPosition
        if self.reverseRotateTalon:
            ticks = -ticks + self.rotateTalonEncoderTicks
        return float(ticks) / float(self.rotateTalonEncoderTicks) * math.pi * 2
        
    def rotateWheel(self, target):
        if self.reverseRotateTalon:
            target = -target
        
        targetTicks = target / (math.pi * 2) * self.rotateTalonEncoderTicks \
            + self.rotateTalonInitialPosition
        currentTicks = self.rotateTalon.getPosition()
        diff = targetTicks - currentTicks
        if diff < 0:
            diff = -(abs(diff) % self.rotateTalonEncoderTicks)
        else:
            diff %= self.rotateTalonEncoderTicks
        if diff > self.rotateTalonEncoderTicks / 2:
            diff -= self.rotateTalonEncoderTicks
        if diff < -self.rotateTalonEncoderTicks / 2:
            diff += self.rotateTalonEncoderTicks
                
        self.rotateTalon.set(currentTicks + diff)
    
    def setDriveMode(self, driveMode):
        if driveMode == DriveInterface.DriveMode.POSITION \
                and self.driveMode != DriveInterface.DriveMode.POSITION:
            self.driveTalonJeff.zero()
        seamonsters.drive.setControlMode(self.driveTalon, driveMode)
        self.driveMode = driveMode
        
    def setSpeed(self, speed):
        if self.driveMode == DriveInterface.DriveMode.POSITION:
            self.driveTalonJeff.set(speed)
            self.driveTalonJeff.update()
        else:
            self.driveTalon.set(speed)
    

class SwerveDrive(DriveInterface):
    """
    An implementation of DriveInterface for swerve drives.
    """
    
    def __init__(self):
        DriveInterface.__init__(self)
        self.wheels = [ ]
        self.speedModeVelocity = 2000
        self.positionModeVelocity = 400
        self.invert = False
        
    def setMaxVeloicty(self, velocity):
        """
        Sets the max encoder velocity for position/jeff and speed mode.
        Default is 400. For position mode, this is the maximum difference
        between target and current position for every iteration (50 times per
        second). Speed mode behaves similarly, but since wpilib uses units of
        10ths of a second, the velocity value is multiplied by 5.
        """
        self.speedModeVelocity = velocity * 5
        self.positionModeVelocity = velocity
        
    def invert(self, enabled=True):
        """
        When enabled, the direction of all motors will be reversed.
        """
        self.invert = enabled
    
    def addWheel(self, xLocation, yLocation,
            driveTalon=None, rotateTalon=None, rotateTalonEncoderTicks=None):
        """
        Add a wheel to the robot at the specific location. driveTalon is the
        motor that spins the wheel; rotateTalon is the motor that rotates the
        swerve drive; rotateTalonEncoderTicks is the number of encoder ticks per
        full rotation for that motor. Set this to a negative value to reverse
        the direction of the rotate motor. If none of those are specified, the
        wheel will be added in test mode, in which it only logs events.
        """
        location = (xLocation, yLocation)
        wheelController = None
        if driveTalon == None:
            wheelController = TestWheelController( len(self.wheels) )
        else:
            wheelController = TalonWheelController(driveTalon, rotateTalon,
                    rotateTalonEncoderTicks)
        self.wheels.append( WheelState(location, wheelController) )
    
    def drive(self, magnitude, direction, turn, forceDriveMode = None):
        if forceDriveMode == None:
            forceDriveMode = self.getDriveMode()
        scale = -1 if self.invert else 1
        if forceDriveMode == DriveInterface.DriveMode.SPEED:
            scale *= self.speedModeVelocity
        elif forceDriveMode == DriveInterface.DriveMode.POSITION:
            scale *= self.positionModeVelocity
        for wheel in self.wheels:
            wheel.calcDrive(magnitude, direction, turn)
            wheel.drive(forceDriveMode, scale)
    
    def printWheelState(self):
        """
        Print the vectors each of the wheels are trying to drive towards.
        """
        for i, wheel in enumerate(self.wheels):
            print("Wheel:", i,
                  "Vector:", wheel.driveVector,
                  "Magnitude:", wheel.targetMagnitude,
                  "Direction:", math.degrees(wheel.targetDirection))


def test_swervedrive_forward():
    
    drive = SwerveDrive()
    drive.addWheel(1.0, 1.0)
    drive.addWheel(-1.0, 1.0)
    drive.addWheel(1.0, -1.0)
    drive.addWheel(-1.0, -1.0)
    drive.drive(4, math.radians(90), 0)
    assert drive.wheels[1].targetMagnitude == 4
