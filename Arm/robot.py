__author__ = "jacobvanthoog"

import wpilib
from ArmControl import ArmControl

class TestArmEncoders (wpilib.IterativeRobot):

    def robotInit(self):
        self.Arm1 = wpilib.CANTalon(0)
        self.Arm2 = wpilib.CANTalon(1)
        self.Control = ArmControl(self.Arm1, self.Arm2)
        self.Control.invert1()
        self.Control.invert2()
        self.Control.moveToPosition(20, 17.5)
        self.Joystick = wpilib.Joystick(0)
        self.TargetX = 20
        self.TargetY = 17.5

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        print(self.Arm1.getEncPosition(), "   ", self.Arm2.getEncPosition())

        if self.Joystick.getRawButton(3): #Up
                self.TargetY += 6.0 / 50.0
        elif self.Joystick.getRawButton(2): #Down
                self.TargetY -= 6.0 / 50.0
        elif self.Joystick.getRawButton(5): #Left
                self.TargetX += 6.0 / 50.0
        elif self.Joystick.getRawButton(4): #Right
                self.TargetX -= 6.0 / 50.0

        self.Control.moveToPosition(self.TargetX, self.TargetY)
        self.Control.update()

if __name__ == "__main__":
    wpilib.run(TestArmEncoders)
