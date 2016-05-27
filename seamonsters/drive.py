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

    class DriveMode:
        VOLTAGE = 1
        SPEED = 2
        POSITION = 3
    
    def __init__(self):
        self.driveMode = DriveInterface.DriveMode.SPEED

    def setDriveMode(self, mode):
        self.driveMode = mode

    def getDriveMode(self):
        return self.driveMode
    
    def drive(self, magnitude, direction, turn, forceDriveMode = None):
        pass
