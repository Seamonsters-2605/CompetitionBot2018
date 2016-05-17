__author__ = "jacobvanthoog"

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
