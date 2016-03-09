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
        if self.Joystick.getRawButton(1): #A
            self.Arm.setTarget(self.Arm.getPosition())
        if self.Joystick.getRawButton(2): #B
            self.Arm.update()
        
if __name__ == "__main__":
    wpilib.run(ArmTest)
