__author__ = "jacobvanthoog"

import wpilib
import math

def setControlMode(talon, driveMode):
    """
    Given a DriveInterface.DriveMode, set the control mode of a CANTalon using
    a wpilib.CANTalon.ControlMode.
    """
    if driveMode == DriveInterface.DriveMode.VOLTAGE:
        talon.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
    if driveMode == DriveInterface.DriveMode.SPEED:
        talon.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
    if driveMode == DriveInterface.DriveMode.POSITION:
        talon.changeControlMode(wpilib.CANTalon.ControlMode.Position)

class DriveInterface:
    """
    A generic, abstract interface for driving a robot. Allows 3 different
    control modes for CANTalons, specified by DriveMode.
    DriveMode purposefully doesn't have options for configuring things like the
    maximum velocity of the motors or the ticks-per-rotation for position mode.
    It is assumed each implementation will have methods for this. But assuming
    that has been set up in the robotInit method, all DriveInterface classes
    should be interchangable.
    """


    class DriveMode:
        """
        Control modes for CANTalons. POSITION is incremental position mode (aka
        "Jeff mode").
        """
        VOLTAGE = 1
        SPEED = 2
        POSITION = 3
    
    def __init__(self):
        self.driveMode = DriveInterface.DriveMode.VOLTAGE
        self.magnitudeScale = 1
        self.turnScale = 1

    def setDriveMode(self, mode):
        """
        Set the default control mode for driving. If you call drive() without
        forceDriveMode, this will be used.
        """
        self.driveMode = mode

    def getDriveMode(self):
        """
        Get the current default control mode, as set by setDriveMode(). The
        default is SPEED, but implementations may have their own defaults.
        """
        return self.driveMode
    
    def drive(self, magnitude, direction, turn, forceDriveMode = None):
        """
        Drive the robot, with a given magnitude, direction, and turn.
        If forceDriveMode is specified, the current drive mode will be 
        overriden. It is expected that this function be called in a loop.
        """
        pass

class TestDriveInterface(DriveInterface):

    def drive(self, magnitude, direction, turn, forceDriveMode = None):
        print("Drive mag", magnitude, "dir", direction, "turn", turn)


class AccelerationFilterDrive(DriveInterface):
    """
    Wraps another drive interface, and provides acceleration filtering.
    """
    
    def __init__(self, interface, accelerationRate=.08):
        """
        ``interface`` is the DriveInterface to provide acceleration filtering
        for. ``accelerationRate`` defaults to .08 (0 to full speed in .25
        seconds).
        """
        self.interface = interface
        
        self.accelerationRate = accelerationRate
        self.previousX = 0.0
        self.previousY = 0.0
        self.previousTurn = 0.0
        
    def setDriveMode(self, mode):
        self.interface.setDriveMode(mode)

    def getDriveMode(self):
        return self.interface.getDriveMode()
    
    def drive(self, magnitude, direction, turn, forceDriveMode = None):
        magnitude, direction, turn = \
            self._accelerationFilter(magnitude, direction, turn)
        self.interface.drive(magnitude, direction, turn, forceDriveMode)

    def getFilteredMagnitude(self):
        return math.sqrt(self.previousX ** 2 + self.previousY ** 2)

    def getFilteredDirection(self):
        return math.atan2(self.previousY, self.previousX)

    def getFilteredTurn(self):
        return self.previousTurn
    
    # returns an tuple of: (magnitude, direction, turn)
    def _accelerationFilter(self, magnitude, direction, turn):
        if abs(self.previousTurn - turn) <= self.accelerationRate:
            newTurn = turn
        else:
            if turn > self.previousTurn:
                newTurn = self.previousTurn + self.accelerationRate
            else:
                newTurn = self.previousTurn - self.accelerationRate
        
        x = magnitude * math.cos(direction)
        y = magnitude * math.sin(direction)
        distanceToNew = math.sqrt( (x - self.previousX) ** 2 \
                + (y - self.previousY) ** 2 )

        if distanceToNew <= self.accelerationRate:
            newX = x
            newY = y
            newMagnitude = magnitude
            newDirection = direction
        else:
            directionToNew = math.atan2(y - self.previousY, x - self.previousX)
            newX = self.previousX \
                    + math.cos(directionToNew) * self.accelerationRate
            newY = self.previousY \
                    + math.sin(directionToNew) * self.accelerationRate
            newMagnitude = math.sqrt(newX ** 2 + newY ** 2)
            newDirection = math.atan2(newY, newX)

        self.previousX = newX
        self.previousY = newY
        self.previousTurn = newTurn
        return newMagnitude, newDirection, newTurn

class FieldOrientedDrive(DriveInterface):
    """
    Wraps another drive interface, and provides field orientation.
    """
    
    def __init__(self, interface, ahrs, offset=0.0):
        """
        Create the FieldOrientedDrive with another DriveInterface to wrap and a
        ``robotpy_ext.common_drivers.navx.AHRS``. If given, the offset is a
        value in radians to add to all direction inputs.
        """
        self.interface = interface
        self.ahrs = ahrs
        self.origin = 0.0
        self.offset = offset

    def zero(self):
        self.origin = self._getYawRadians()
        
    def setDriveMode(self, mode):
        self.interface.setDriveMode(mode)

    def getDriveMode(self):
        return self.interface.getDriveMode()
    
    def drive(self, magnitude, direction, turn, forceDriveMode = None):
        robotAngle = self._getYawRadians() - self.origin
        direction -= robotAngle
        direction += self.offset
        self.interface.drive(magnitude, direction, turn, forceDriveMode)
    
    def _getYawRadians(self):
        return - math.radians(self.ahrs.getYaw())

if __name__ == "__main__":
    # test acceleration filter drive
    filterDrive = AccelerationFilterDrive(TestDriveInterface())
    for i in range(0, 20):
        filterDrive.drive(1.0, 1.0, 1.0)
