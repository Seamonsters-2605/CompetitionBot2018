__author__ = "jacobvanthoog"

import wpilib
from seamonsters.drive import DriveInterface
from seamonsters.gamepad import Gamepad

class DriveTest (wpilib.IterativeRobot):
    
    def robotInit(self):
        self.movegamepad = Gamepad(port = 0)
        self.drive = None
        
    def initDrive(self, drive):
        self.drive = drive
        self.drive.setDriveMode(DriveInterface.DriveMode.POSITION)
        
    def teleopPeriodic(self):
        if self.drive == None:
            return
        
        slowed = 0
        if self.movegamepad.getRawButton(Gamepad.LJ): # faster button
            slowed = 1
        elif self.movegamepad.getRawButton(Gamepad.LB): # slower button
            slowed = .2
        else: # no button pressed
            slowed = .55
        # change drive mode with A, B, and X
        if   self.movegamepad.getRawButton(Gamepad.A):
            self.drive.setDriveMode(DriveInterface.DriveMode.VOLTAGE)
        elif self.movegamepad.getRawButton(Gamepad.B):
            self.drive.setDriveMode(DriveInterface.DriveMode.SPEED)
        elif self.movegamepad.getRawButton(Gamepad.X):
            self.drive.setDriveMode(DriveInterface.DriveMode.POSITION)
        
        turn = -self.movegamepad.getRX() * abs(self.movegamepad.getRX()) \
            * (slowed / 2)
        magnitude = self.movegamepad.getLMagnitude()**2 * slowed
        direction = self.movegamepad.getLDirection()
        
        self.drive.drive(magnitude, direction, turn)
