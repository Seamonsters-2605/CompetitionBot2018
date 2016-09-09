__author__ = "jacobvanthoog"

import wpilib
from seamonsters.drive import DriveInterface
from seamonsters.gamepad import Gamepad

class DriveTest (wpilib.IterativeRobot):
    
    def robotInit(self):
        self.gamepad = Gamepad(port = 0)
        self.drive = None
        
    def initDrive(self, drive, driveMode=DriveInterface.DriveMode.POSITION):
        self.drive = drive
        self.drive.setDriveMode(driveMode)
        
    def teleopPeriodic(self):
        if self.drive == None:
            return
        
        # change drive mode with A, B, and X
        if   self.gamepad.getRawButton(Gamepad.A):
            self.drive.setDriveMode(DriveInterface.DriveMode.VOLTAGE)
        elif self.gamepad.getRawButton(Gamepad.B):
            self.drive.setDriveMode(DriveInterface.DriveMode.SPEED)
        elif self.gamepad.getRawButton(Gamepad.X):
            self.drive.setDriveMode(DriveInterface.DriveMode.POSITION)
        
        scale = .55
        if self.gamepad.getRawButton(Gamepad.LJ): # faster button
            scale = 1
        elif self.gamepad.getRawButton(Gamepad.LB): # slower button
            scale = .2
        
        turn = -self.gamepad.getRX() * abs(self.gamepad.getRX()) \
            * (scale / 2)
        magnitude = self.gamepad.getLMagnitude()**2 * scale
        direction = self.gamepad.getLDirection()
        
        self.drive.drive(magnitude, direction, turn)
