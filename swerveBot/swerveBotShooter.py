__author__ = "jacobvanthoog"

from seamonsters.wpilib_sim import simulate
from seamonsters.gamepad import Gamepad
import Shooter.ShootController
import wpilib

class SwerveBotShooter(wpilib.IterativeRobot):
    
    def robotInit(self):
        self.gamepad = Gamepad(1)
        
        self.LeftFly = wpilib.CANTalon(4)
        self.RightFly = wpilib.CANTalon(5)
        self.LimitSwitch = wpilib.DigitalInput(0)
        self.LimitSwitch2 = wpilib.DigitalInput(1)
        self.Intake = wpilib.CANTalon(8)
        self.Shooter = Shooter.ShootController.ShootController(\
            self.LeftFly, self.RightFly,\
            self.Intake, self.LimitSwitch, self.LimitSwitch2)
        
    def teleopPeriodic(self):
        self.Shooter.update(self.gamepad.getRawButton(Gamepad.B),\
                            self.gamepad.getRawButton(Gamepad.X),\
                            self.gamepad.getRawButton(Gamepad.A),\
                            self.gamepad.getRawButton(Gamepad.Y))
        
        
if __name__ == "__main__":
    wpilib.run(SwerveBotShooter)
