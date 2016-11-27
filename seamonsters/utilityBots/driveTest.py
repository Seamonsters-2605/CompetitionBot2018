__author__ = "jacobvanthoog"

import wpilib
from seamonsters.drive import DriveInterface
from seamonsters.gamepad import Gamepad

class DriveTest (wpilib.IterativeRobot):
    
    def robotInit(self, normalScale=.5, fastScale=1.0, slowScale=.2):
        """
        ``normalScale``, ``fastScale`` and ``slowScale`` are optional - these
        are the scales (from 0.0 to 1.0) for drive speed when driving normally,
        when the Fast button is pressed, and when the Slow button is pressed.
        """
        print("Left Bumper: Slower")
        print("Left Joystick: Faster")
        self.gamepad = Gamepad(port = 0)
        self.drive = None

        self.normalScale = normalScale
        self.fastScale = fastScale
        self.slowScale = slowScale
        
        self.talons = [ ]
        self.currentPID = None
        self.normalPID = None
        self.slowPID = None
        
    def initDrive(self, drive, driveMode=DriveInterface.DriveMode.POSITION,
                        talons=[ ], normalPID=None, slowPID=None):
        """
        ``drive`` is a ``seamonsters.drive.DriveInterface``. ``driveMode`` is a
        ``seamonsters.drive.DriveInterface.DriveMode`` - if given, this is the
        initial drive mode that the DriveInterface is set to. ``talons`` is a
        list of CANTalons (you only need to specify this if you want to use
        alternate slow-mode PIDs). ``normalPID`` and ``slowPID`` should be
        tuples of 4 floats (P, I, D, F). ``slowPID`` is used while the Slow
        button is pressed. Both are optional.
        """
        self.drive = drive
        self.drive.setDriveMode(driveMode)
        
        self.talons = talons
        self.currentPID = None
        self.normalPID = normalPID
        self.slowPID = slowPID
        
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
        if self.gamepad.getRawButton(Gamepad.LB): # slower button
            scale = self.slowScale
            self._setPID(self.slowPID)
        else:
            self._setPID(self.normalPID)
        
        turn = -self.gamepad.getRX() * abs(self.gamepad.getRX()) \
            * (scale / 2)
        magnitude = self.gamepad.getLMagnitude()**2 * scale
        direction = self.gamepad.getLDirection()
        
        self.drive.drive(magnitude, direction, turn)
        
    def _setPID(self, pid):
        if pid == None:
            return
        if pid == self.currentPID:
            return
        self.currentPID = pid
        for talon in self.talons:
            talon.setPID(pid[0], pid[1], pid[2], pid[3])

