__author__ = "jacobvanthoog"

import wpilib

class Test(wpilib.IterativeRobot):
    def robotInit(self):
        wpilib.SmartDashboard.putString("thisIsAKey", "this is a value!")
        self.Talon1 = wpilib.CANTalon(1)
        self.Talon1.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.Talon2 = wpilib.CANTalon(3)
        self.Talon2.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)

    def teleopPeriodic(self):
        print(self.Talon1.getPosition(), self.Talon2.getPosition())
        
if __name__ == "__main__":
    wpilib.run(Test)
