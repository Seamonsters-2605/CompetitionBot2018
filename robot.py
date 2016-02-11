__author__ = "jacobvanthoog"

import math
import wpilib
import JoystickLib.joystickLib
from HolonomicDrive.HolonomicDrive import HolonomicDrive
from Shooter import ShootController, Flywheels, Intake
from PDPLogger.PDPLogger import PDPLogger

class MainRobot (wpilib.IterativeRobot):

    def robotInit(self):
        self.FL = wpilib.CANTalon(2)
        self.FR = wpilib.CANTalon(1)
        self.BL = wpilib.CANTalon(0)
        self.BR = wpilib.CANTalon(3)
        self.FL.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.FR.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.BL.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.BR.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.FL.setPID(.5, 0.0, 4.0, 0.0)
        self.FR.setPID(.5, 0.0, 4.0, 0.0)
        self.BL.setPID(.5, 0.0, 4.0, 0.0)
        self.BR.setPID(.5, 0.0, 4.0, 0.0)

        self.MoveJoy = JoystickLib.joystickLib.createJoystick(0)
        self.MoveJoy.invertY()
        self.TurnJoy = JoystickLib.joystickLib.createJoystick(1)
        self.TurnJoy.invertY()

        self.Drive = HolonomicDrive(self.FL, self.FR, self.BL, self.BR)
        self.Drive.invertDrive(True)
        self.Drive.setWheelOffset(math.radians(27))
        self.Drive.setDriveMode(HolonomicDrive.DriveMode.JEFF)

        self.LeftFly = wpilib.CANTalon(4)
        self.RightFly = wpilib.CANTalon(5)
        self.LimitSwitch = wpilib.DigitalInput(0)
        self.Intake = wpilib.CANTalon(8)
        self.Shooter = ShootController.ShootController(self.LeftFly, self.RightFly,\
                                       self.Intake, self.LimitSwitch)
        self.Shooter.invertFlywheels()

        self.Logger = PDPLogger(wpilib.PowerDistibutionPanel(0))

        
        

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.Drive.zeroEncoderTargets()

    def teleopPeriodic(self):
        self.TurnJoy.updateButtons();
        self.MoveJoy.updateButtons();
        turn = -self.TurnJoy.getX()
        magnitude = self.MoveJoy.getMagnitude()
        direction = self.MoveJoy.getDirection()
        self.Drive.drive(magnitude, direction, turn)
        self.Shooter.update(self.MoveJoy.getRawButton(2),\
                            self.MoveJoy.getRawButton(3),\
                            self.MoveJoy.getTrigger())
        self.Logger.printCurrents()

if __name__ == "__main__":
    wpilib.run(MainRobot)

