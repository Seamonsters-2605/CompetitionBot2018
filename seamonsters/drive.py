__author__ = "jacobvanthoog"

import wpilib

def setControlMode(talon, driveMode):
    if driveMode == DriveInterface.DriveMode.VOLTAGE:
        talon.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
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
