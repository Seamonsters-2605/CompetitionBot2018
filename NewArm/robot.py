__author__ = "jacobvanthoog"

import wpilib
from NewArmControl import Arm

class ArmTest(wpilib.IterativeRobot):
    
    def robotInit(self):
        pass
    
    def autonomousInit(self):
        pass
    
    def autonomousPeriodic(self):
        pass
    
    def teleopInit(self):
        self.CAN = wpilib.CANTalon(0)
        self.Arm = Arm(self.CAN)
        self.Joystick = wpilib.Joystick(0)
    
    def teleopPeriodic(self):
        print(self.CAN.getEncPosition(), self.CAN.getPosition())
        if self.Joystick.getRawButton(1):
            self.Arm.update()
        if self.Joystick.getRawButton(2):
            self.Arm.setTarget(self.Arm.getPosition())
        if self.Joystick.getRawButton(5):
            self.Arm.movePosition(4000)
        if self.Joystick.getRawButton(4):
            self.Arm.movePosition(-4000)
        
if __name__ == "__main__":
    wpilib.run(ArmTest)
