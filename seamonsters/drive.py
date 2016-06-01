__author__ = "jacobvanthoog"

import wpilib

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
        self.driveMode = DriveInterface.DriveMode.SPEED
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
        
    def setMagnitudeScale(self, scale):
        """
        Setting the magnitudeScale causes the magnitude in future calls to
        drive() to be scaled by a certain amount (which could be negative). This
        must be done by implementations!
        """
        self.magnitudeScale = scale
        
    def getMagnitudeScale(self):
        return self.magnitudeScale
        
    def setTurnScale(self, scale):
        """
        Setting the turnScale causes the turn amound in future calls to
        drive() to be scaled by a certain amount (which could be negative). This
        must be done by implementations!
        """
        self.turnScale = scale
        
    def getTurnScale(self):
        return self.turnScale
    
    def drive(self, magnitude, direction, turn, forceDriveMode = None):
        """
        Drive the robot, with a given magnitude, direction, and turn.
        If forceDriveMode is specified, the current drive mode will be 
        overriden. It is expected that this function be called in a loop.
        """
        pass
