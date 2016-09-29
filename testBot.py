__author__ = "jacobvanthoog"

from seamonsters.gamepad import Gamepad
import wpilib

class Test(wpilib.IterativeRobot):
    def robotInit(self):
        wpilib.SmartDashboard.putString("thisIsAKey", "this is a value!")
        self.Gamepad = Gamepad(0)

    def teleopPeriodic(self):
        print(self.Gamepad.getLX(), self.Gamepad.getLY(),
              self.Gamepad.getRX(), self.Gamepad.getRY())
        
if __name__ == "__main__":
    wpilib.run(Test)
