__author__ = "jacobvanthoog"

import wpilib
from .ArmControl import ArmControl

class TestArmEncoders (wpilib.IterativeRobot):

    def robotInit(self):
        self.Arm1 = wpilib.CANTalon(6)
        self.Arm2 = wpilib.CANTalon(7)
        self.Control = ArmControl(self.Arm1, self.Arm2)
        self.Control.moveToPosition(20, 17.5)
    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        print(self.Arm1.getEncPosition(), "   ", self.Arm2.getEncPosition())
        #self.Control.update()

if __name__ == "__main__":
    wpilib.run(TestArmEncoders)