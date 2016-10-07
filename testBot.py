__author__ = "jacobvanthoog"

from seamonsters.gamepad import Gamepad
from seamonsters.utilityBots.pidTest import PIDTest
import wpilib

class Test(PIDTest):
    def __init__(self):
        super().__init__(4)
        #wpilib.SmartDashboard.putString("thisIsAKey", "this is a value!")
        
if __name__ == "__main__":
    wpilib.run(Test)
