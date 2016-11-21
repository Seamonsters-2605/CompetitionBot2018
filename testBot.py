__author__ = "jacobvanthoog"

import wpilib
from robotpy_ext.common_drivers.navx import AHRS
from seamonsters.logging import LogState

class Test(wpilib.IterativeRobot):

    def robotInit(self):
        self.ahrs = AHRS.create_spi() # the NavX
        #self.ahrs = AHRS.create_i2c() # use this instead?
        
        self.yawLog = LogState("Yaw")
        self.angleLog = LogState("Angle")
        
        #wpilib.SmartDashboard.putString("thisIsAKey", "this is a value!")
        
    def teleopPeriodic(self):
        self.yawLog.update(ahrs.getYaw())
        self.angleLog.update(ahrs.getAngle())
        
if __name__ == "__main__":
    wpilib.run(Test)
