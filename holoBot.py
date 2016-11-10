__author__ = "jacobvanthoog"

from seamonsters.wpilib_sim import simulate
from seamonsters.utilityBots.driveTest import DriveTest
from seamonsters.drive import DriveInterface
from seamonsters.drive import AccelerationFilterDrive
from seamonsters.holonomicDrive import HolonomicDrive
import wpilib
import math

class SwerveBot(DriveTest):
    
    def robotInit(self):
        DriveTest.robotInit(self, normalScale = .3, fastScale = .5,
                            slowScale = .05)
        
        fl = wpilib.CANTalon(2)
        fr = wpilib.CANTalon(1)
        bl = wpilib.CANTalon(0)
        br = wpilib.CANTalon(3)
        fl.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        fr.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        bl.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        br.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        fl.setPID(1.0, 0.0, 3.0, 0.0)
        fr.setPID(1.0, 0.0, 3.0, 0.0)
        bl.setPID(1.0, 0.0, 3.0, 0.0)
        br.setPID(1.0, 0.0, 3.0, 0.0)
        
        # 4156 ticks per wheel rotation
        # encoder has 100 raw ticks -- with a QuadEncoder that makes 400 ticks
        # the motor gear has 18 teeth and the wheel has 187 teeth
        # 187 / 18 * 400 = 4155.5556 = ~4156
        drive = HolonomicDrive(fl, fr, bl, br, 4156)
        drive.invertDrive(True)
        # TODO: move magic number to constant
        drive.setWheelOffset(math.radians(22.5)) #angle of rollers
        
        filterDrive = AccelerationFilterDrive(drive)
        
        DriveTest.initDrive(self, filterDrive,
                            driveMode=DriveInterface.DriveMode.POSITION)
        
        
if __name__ == "__main__":
    wpilib.run(SwerveBot)
