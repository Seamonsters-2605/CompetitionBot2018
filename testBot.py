__author__ = "jacobvanthoog"

from seamonsters.gamepad import Gamepad
import wpilib

class Test(wpilib.IterativeRobot):
    def robotInit(self):
        wpilib.SmartDashboard.putString("thisIsAKey", "this is a value!")
        self.Talon1 = wpilib.CANTalon(1)
        self.Talon1.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.Talon2 = wpilib.CANTalon(3)
        self.Talon2.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.Gamepad = Gamepad(0)

    def teleopPeriodic(self):
        #print(self.Talon1.getPosition(), self.Talon2.getPosition())
        print(self.Gamepad.getRawButton(Gamepad.UP),
              self.Gamepad.getRawButton(Gamepad.DOWN),
              self.Gamepad.getRawButton(Gamepad.LEFT),
              self.Gamepad.getRawButton(Gamepad.RIGHT),
              self.Gamepad.getRawButton(Gamepad.LT),
              self.Gamepad.getRawButton(Gamepad.RT))
        
if __name__ == "__main__":
    wpilib.run(Test)
