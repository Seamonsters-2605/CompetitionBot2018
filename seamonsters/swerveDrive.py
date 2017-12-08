__author__ = "jacobvanthoog"

from seamonsters.drive import DriveInterface
import seamonsters.drive
from seamonsters.motorControl import *
import math
import ctre

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
    
    def drive(self):
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
        mag = self.targetMagnitude
        if self.invertMagnitude:
            mag = -mag
        self.controller.setSpeed(mag)


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
        Spin the wheel at the specific speed, between -1 and 1
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
    A wheel controller controlling two CANTalons. Uses a MotorSpeedControl.
    """
    
    def __init__(self, driveController, rotateTalon, rotateTalonEncoderTicks):
        """
        driveController should be a MotorSpeedControl
        """
        self.driveController = driveController
        
        self.rotateTalon = rotateTalon
        self.rotateTalonInitialPosition = rotateTalon.getPosition()
        self.rotateTalonEncoderTicks = abs(rotateTalonEncoderTicks)
        self.reverseRotateTalon = rotateTalonEncoderTicks < 0
        rotateTalon.changeControlMode(ctre.CANTalon.ControlMode.Position)
        
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
        
    def setSpeed(self, speed):
        self.driveController.set(speed)
        self.driveController.update()
    

class SwerveDrive(DriveInterface):
    """
    An implementation of DriveInterface for swerve drives.
    """
    
    def __init__(self):
        self.wheels = [ ]
        self.manager = MotorManager()
        self.driveMode = DriveInterface.DriveMode.VOLTAGE
        
    def setMaxVeloicty(self, velocity):
        """
        Sets the max encoder velocity for position/jeff and speed mode.
        Default is 400. For position mode, this is the maximum difference
        between target and current position for every iteration (50 times per
        second). Speed mode behaves similarly, but since wpilib uses units of
        10ths of a second, the velocity value is multiplied by 5.
        """
        self.manager.setMaxSpeed(velocity)

    def setDriveMode(self, mode):
        self.driveMode = mode
        self.manager.setDriveMode(mode)
    
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
            multiMode = self.manager.addMotor(driveTalon)
            wheelController = TalonWheelController(multiMode, rotateTalon,
                    rotateTalonEncoderTicks)
        self.wheels.append( WheelState(location, wheelController) )
    
    def drive(self, magnitude, direction, turn):
        mode = self.driveMode
        self.manager.setDriveMode(mode)
        for wheel in self.wheels:
            wheel.calcDrive(magnitude, direction, turn)
            wheel.drive()
    
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
