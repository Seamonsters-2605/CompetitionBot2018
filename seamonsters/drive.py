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


class AccelerationFilterDrive(DriveInterface):
    """
    Wraps another drive interface, and provides acceleration filtering.
    """
    
    def __init__(self, interface):
        """
        ``interface`` is the DriveInterface to provide acceleration filtering
        for.
        """
        self.interface = interface
        
        self.maximumAccelDistance = .08
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
    
    # returns an tuple of: (magnitude, direction, turn)
    def _accelerationFilter(self, magnitude, direction, turn):
        newX = magnitude * math.cos(direction)
        newY = magnitude * math.sin(direction)
        distanceToNew = math.sqrt( (newX - self.previousX) ** 2 \
                + (newY - self.previousY) ** 2 )
        finalTurn = turn
        if not abs(self.previousTurn - turn) <= self.maximumAccelDistance:
            if turn > self.previousTurn:
                finalTurn = self.previousTurn + self.maximumAccelDistance
            else:
                finalTurn = self.previousTurn - self.maximumAccelDistance

        if (distanceToNew <= self.maximumAccelDistance):
            self.previousX = newX
            self.previousY = newY
            self.previousTurn = finalTurn
            return magnitude, direction, finalTurn

        #Alternate Return for strafe fail to pass
        directionToNew = math.atan2(newY-self.previousY, newX-self.previousX)
        finalX = self.previousX \
                + math.cos(directionToNew) * self.maximumAccelDistance
        finalY = self.previousY \
                + math.sin(directionToNew) * self.maximumAccelDistance
        self.previousX = finalX
        self.previousY = finalY
        self.previousTurn = finalTurn
        return math.sqrt(finalX ** 2 + finalY ** 2), \
               math.atan2(finalY, finalX), \
               finalTurn

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

