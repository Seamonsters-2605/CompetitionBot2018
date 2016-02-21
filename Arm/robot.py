__author__ = "jacobvanthoog"

import wpilib

class TestArmEncoders (wpilib.IterativeRobot):

    def robotInit(self):
        self.Arm1 = wpilib.CANTalon(6)
        self.Arm2 = wpilib.CANTalon(7)
    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        print(self.Arm1.getEncPosition(), "   ", self.Arm2.getEncPosition())

if __name__ == "__main__":
    wpilib.run(TestArmEncoders)