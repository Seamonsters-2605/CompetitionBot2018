__author__ = "jacobvanthoog"

from seamonsters.utilityBots.driveTest import DriveTest
from seamonsters.drive import DriveInterface
from seamonsters.swerveDrive import SwerveDrive
import wpilib

class SwerveBot(DriveTest):
    
    def robotInit(self):
        DriveTest.robotInit(self)
        
        # Front Right wheel
        frDrive = wpilib.CANTalon(2)
        frDrive.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        frDrive.setPID(1.0, 0.0, 3.0, 0.0)
        
        frRotate = wpilib.CANTalon(1)
        frRotate.reverseOutput(True)
        frRotate.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        frRotate.setPID(1.0, 0.0, 3.0, 0.0)
        
        
        # Back Left wheel
        blDrive = wpilib.CANTalon(3)
        blDrive.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        blDrive.setPID(1.0, 0.0, 3.0, 0.0)
        
        blRotate = wpilib.CANTalon(0)
        blRotate.reverseOutput(True)
        blRotate.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        blRotate.setPID(1.0, 0.0, 3.0, 0.0)
        
        # Drive controller
        drive = SwerveDrive()
        
        # 104 gear teeth / 18 gear teeth * 280 ticks per rotation * 4 (quad)
        # then divide by 2 for some reason
        drive.addWheel(1.0, 1.0, frDrive, frRotate, -104/18*280*4/2)
        drive.addWheel(1.0, -1.0, blDrive, blRotate, -104/18*280*4/2)
        
        DriveTest.initDrive(self, drive)
        drive.setDriveMode(DriveInterface.DriveMode.VOLTAGE)
        
        
if __name__ == "__main__":
    wpilib.run(SwerveBot)
