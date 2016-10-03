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

        self.motorSpeed = 0
        self.lastPrintedSpeedString = ""
        self.hold = False
        
    def teleopPeriodic(self):
        if not self.hold:
            buttonPressed = False
            speed = 3
            if self.gamepad.getRawButton(Gamepad.A):
                buttonPressed = True
                speed += 1
            if self.gamepad.getRawButton(Gamepad.B):
                buttonPressed = True
                speed += 2
            if self.gamepad.getRawButton(Gamepad.X):
                buttonPressed = True
                speed += 4
            if self.gamepad.getRawButton(Gamepad.Y):
                buttonPressed = True
                speed += 8
            
            if buttonPressed:
                self.motorSpeed = -float(speed) / 18.0
            else:
                self.motorSpeed = 0.0

            if self.getFlywheelSpeedString() != self.lastPrintedSpeedString:
                self.lastPrintedSpeedString = self.getFlywheelSpeedString()
                print("Flywheels running at", self.lastPrintedSpeedString)
        
        self.RightFly.set(self.motorSpeed)
        self.LeftFly.set(self.motorSpeed)

        if not self.hold and self.gamepad.getRawButton(Gamepad.START):
            self.hold = True
            print("Hold flywheel speed at", self.getFlywheelSpeedString())
        elif self.hold and self.gamepad.getRawButton(Gamepad.BACK):
            self.hold = False
            print("Hold disabled")
            
        if self.gamepad.getRawButton(Gamepad.RB):
            # intake forwards
            self.Intake.set(.5)
        elif self.gamepad.getRawButton(Gamepad.LB):
            # intake backwards
            self.Intake.set(-.5)
        else:
            self.Intake.set(0.0)

    def getFlywheelSpeedString(self):
        return str(int(round(-self.motorSpeed * 100))) + "%"
            
        
        
if __name__ == "__main__":
    wpilib.run(SwerveBotShooter)
