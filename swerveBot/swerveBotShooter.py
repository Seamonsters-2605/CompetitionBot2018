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
        self.LeftFly.setPID(1, 0.0009, 1, 0.0)
        self.RightFly.setPID(1, 0.0009, 1, 0.0)
        self.LeftFly.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        self.RightFly.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        
        self.Intake = wpilib.CANTalon(8)
        self.Intake.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        
    def teleopPeriodic(self):
        speed = 0
        if self.gamepad.getRawButton(Gamepad.A):
            speed += 1
        if self.gamepad.getRawButton(Gamepad.B):
            speed += 2
        if self.gamepad.getRawButton(Gamepad.X):
            speed += 4
        if self.gamepad.getRawButton(Gamepad.Y):
            speed += 8
        motorSpeed = -float(speed) / 15.0
        self.RightFly.set(motorSpeed)
        self.LeftFly.set(motorSpeed)
            
        if self.gamepad.getRawButton(Gamepad.LB):
            # intake forwards
            self.Intake.set(.5)
        elif self.gamepad.getRawButton(Gamepad.RB):
            # intake backwards
            self.Intake.set(-.5)
        else:
            self.Intake.set(0.0)
        
            
        
        
if __name__ == "__main__":
    wpilib.run(SwerveBotShooter)
