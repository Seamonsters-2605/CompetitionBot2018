__author__ = "jacobvanthoog"

import seamonsters.gamepad
import wpilib

class Test(wpilib.IterativeRobot):
    def robotInit(self):
        wpilib.SmartDashboard.putString("thisIsAKey", "this is a value!")
        self.Talon1 = wpilib.CANTalon(1)
        self.Talon1.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.Talon2 = wpilib.CANTalon(3)
        self.Talon2.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.Gamepad = seamonsters.gamepad.Gamepad(0)

    def teleopPeriodic(self):
        print(self.Talon1.getPosition(), self.Talon2.getPosition())
        #print(self.Gamepad.getLX(), self.Gamepad.getLY(),
        #      self.Gamepad.getLDirection(),
        #      self.Gamepad.getRX(), self.Gamepad.getRY(),
        #      self.Gamepad.getRDirection())
        
if __name__ == "__main__":
    wpilib.run(Test)
