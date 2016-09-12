__author__ = "jacobvanthoog"

from seamonsters.wpilib_sim import simulate
import wpilib

class SwerveBotShooter(wpilib.IterativeRobot):
    
    def robotInit(self):
        pass
            
    def teleopPeriodic(self):
        pass
        
        
if __name__ == "__main__":
    wpilib.run(SwerveBotDrive)
