__author__ = "jacobvanthoog"

import wpilib, math
from ArmControl import ArmControl

class TestArmEncoders (wpilib.IterativeRobot):

    def robotInit(self):
        self.Arm1 = wpilib.CANTalon(0)
        self.Arm2 = wpilib.CANTalon(1)
        self.Control = ArmControl(self.Arm1, self.Arm2)
        self.Control.setOffset1(-math.pi)
        #self.Control.moveToPosition(20, 17.5)
        #self.Control.moveMotorRotation(math.pi/2, math.pi/2)
        self.Joystick = wpilib.Joystick(0)
        self.TargetX = math.atan2(20,17.5)
        self.TargetY = math.sqrt(20**2 + 17.5**2) #mag

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        #print(self.Arm1.getEncPosition(), "   ", self.Arm2.getEncPosition())

        if self.Joystick.getRawButton(4): #Up
            self.TargetY += 6.0 / 50.0
            print("Up!")
        elif self.Joystick.getRawButton(1): #Down
            self.TargetY -= 6.0 / 50.0
            print("Down!")
        elif self.Joystick.getRawButton(3): #Left
            self.TargetX -= 1.0 / 50.0
            print("Left")
        elif self.Joystick.getRawButton(2): #Right
            self.TargetX += 1.0 / 50.0
            print("Right")

        self.Control.moveTo(self.TargetY, self.TargetX)
        self.Control.update()

if __name__ == "__main__":
    wpilib.run(TestArmEncoders)
