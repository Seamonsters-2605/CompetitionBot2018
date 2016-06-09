__author__ = "jacobvanthoog"

from seamonsters.utilityBots.driveTest import DriveTest
from seamonsters.drive import DriveInterface
from seamonsters.swerveDrive import SwerveDrive
import wpilib

class SwerveBot(DriveTest):
    
    def robotInit(self):
        DriveTest.robotInit(self)
        
        flDrive = wpilib.CANTalon(0)
        flRotate = wpilib.CANTalon(1)
        brDrive = wpilib.CANTalon(2)
        brRotate = wpilib.CANTalon(3)
        flDrive.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        flRotate.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        brDrive.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        flRotate.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        flDrive.setPID(1.0, 0.0, 3.0, 0.0)
        flRotate.setPID(1.0, 0.0, 3.0, 0.0)
        brDrive.setPID(1.0, 0.0, 3.0, 0.0)
        brRotate.setPID(1.0, 0.0, 3.0, 0.0)
        
        drive = SwerveDrive()
        
        # 104 gear teeth / 18 gear teeth * 280 ticks per rotation * 4 (quad)
        drive.addWheel(-1.0, 1.0, flDrive, flRotate, 104/18*280*4)
        drive.addWheel(1.0, -1.0, brDrive, brRotate, 104/18*280*4)
        drive.setDriveMode(DriveInterface.DriveMode.VOLTAGE)
        
        DriveTest.initDrive(self, drive)
        
        
if __name__ == "__main__":
    wpilib.run(SwerveBot)