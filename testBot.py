__author__ = "jacobvanthoog"

from seamonsters.nav6 import nav6
import wpilib

class Test(wpilib.IterativeRobot):
    def robotInit(self):
        wpilib.SmartDashboard.putString("thisIsAKey", "this is a value!")
        
if __name__ == "__main__":
    wpilib.run(Test)
