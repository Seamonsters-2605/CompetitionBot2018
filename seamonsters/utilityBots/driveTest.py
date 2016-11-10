__author__ = "jacobvanthoog"

import wpilib
from seamonsters.drive import DriveInterface
from seamonsters.gamepad import Gamepad

class DriveTest (wpilib.IterativeRobot):
    
    def robotInit(self, normalScale=.5, fastScale=1.0, slowScale=.2):
        print("Left Bumper: Slower")
        print("Left Joystick: Faster")
        self.gamepad = Gamepad(port = 0)
        self.drive = None

        self.normalScale = normalScale
        self.fastScale = fastScale
        self.slowScale = slowScale
        
    def initDrive(self, drive, driveMode=DriveInterface.DriveMode.POSITION):
        self.drive = drive
        self.drive.setDriveMode(driveMode)
        
    def teleopPeriodic(self):
        if self.drive == None:
            return
        
        # change drive mode with A, B, and X
        if   self.gamepad.getRawButton(Gamepad.A):
            print("Voltage mode!")
            self.drive.setDriveMode(DriveInterface.DriveMode.VOLTAGE)
        elif self.gamepad.getRawButton(Gamepad.B):
            print("Speed mode!")
            self.drive.setDriveMode(DriveInterface.DriveMode.SPEED)
        elif self.gamepad.getRawButton(Gamepad.X):
            print("Position mode!")
            self.drive.setDriveMode(DriveInterface.DriveMode.POSITION)
        
        scale = self.normalScale
        if self.gamepad.getRawButton(Gamepad.LJ): # faster button
            scale = self.fastScale
        elif self.gamepad.getRawButton(Gamepad.LB): # slower button
            scale = self.slowScale
        
        turn = -self.gamepad.getRX() * abs(self.gamepad.getRX()) \
            * (scale / 2)
        magnitude = self.gamepad.getLMagnitude()**2 * scale
        direction = self.gamepad.getLDirection()
        
        self.drive.drive(magnitude, direction, turn)
