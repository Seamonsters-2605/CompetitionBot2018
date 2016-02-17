__author__ = "jacobvanthoog"

import math
import wpilib
from wpilib import PowerDistributionPanel
import JoystickLib.joystickLib
from HolonomicDrive.HolonomicDrive import HolonomicDrive
from Shooter import ShootController, Flywheels, Intake
from PDPLogger.PDPLogger import PDPLogger
from JoystickLib.Gamepad import Gamepad

class MainRobot (wpilib.IterativeRobot):

    def robotInit(self):
        self.usinggamepad = True
        self.FL = wpilib.CANTalon(2)
        self.FR = wpilib.CANTalon(1)
        self.BL = wpilib.CANTalon(0)
        self.BR = wpilib.CANTalon(3)
        self.FL.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.FR.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.BL.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.BR.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.FL.setPID(1.0, 0.0, 3.0, 0.0)
        self.FR.setPID(1.0, 0.0, 3.0, 0.0)
        self.BL.setPID(1.0, 0.0, 3.0, 0.0)
        self.BR.setPID(1.0, 0.0, 3.0, 0.0)

        self.movegamepad = JoystickLib.Gamepad.Gamepad(port = 0)
        self.shootgamepad = JoystickLib.Gamepad.Gamepad(port = 1)

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
        self.LimitSwitch2 = wpilib.DigitalInput(1)
        self.Intake = wpilib.CANTalon(8)
        self.Shooter = ShootController.ShootController(\
            self.LeftFly, self.RightFly,\
            self.Intake, self.LimitSwitch, self.LimitSwitch2)
        #self.Shooter.invertFlywheels()

        self.Logger = PDPLogger(PowerDistributionPanel(0))

    

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.Drive.zeroEncoderTargets()

    def teleopPeriodic(self):
        if self.usinggamepad == False: # using joystick
            self.TurnJoy.updateButtons();
            self.MoveJoy.updateButtons();
            turn = -self.TurnJoy.getX()
            magnitude = self.MoveJoy.getMagnitude()
            direction = self.MoveJoy.getDirection()
            self.Drive.drive(magnitude, direction, turn) # jeff mode
            self.Shooter.update(self.MoveJoy.getRawButton(2),\
                            self.MoveJoy.getRawButton(3),\
                            self.MoveJoy.getTrigger(),\
                            self.MoveJoy.getRawButton(5))
            
        else: # using gamepad
            if self.movegamepad.getButtonByLetter("LT"): # faster button
                 self.slowed = 1
            elif self.movegamepad.getButtonByLetter("LB"): # slower button
                self.slowed = .2
            else: # no button pressed
                self.slowed = .55

            # switch drive mode with gamepad
            if   self.movegamepad.getRawButton(Gamepad.A):
                self.Drive.setDriveMode(HolonomicDrive.DriveMode.VOLTAGE)
            elif self.movegamepad.getRawButton(Gamepad.B):
                self.Drive.setDriveMode(HolonomicDrive.DriveMode.SPEED)
            elif self.movegamepad.getRawButton(Gamepad.X):
                self.Drive.setDriveMode(HolonomicDrive.DriveMode.JEFF)
            print(str(self.Drive.getDriveMode()))
            turn = -self.movegamepad.getRX() * self.slowed
            magnitude = self.movegamepad.getLMagnitude() * self.slowed
            direction = self.movegamepad.getLDirection()
            #self.Drive.drive(magnitude, direction, turn)
            self.Drive.driveSpeedJeffMode(magnitude, direction, turn,  self.movegamepad.getRawButton(Gamepad.START))
            self.Shooter.update(self.shootgamepad.getButtonByLetter("B"),\
                                self.shootgamepad.getButtonByLetter("X"),\
                                self.shootgamepad.getButtonByLetter("RB"),\
                                self.shootgamepad.getButtonByLetter("LB"))
            print ("Slowed:" + str(self.slowed))
            print ("FL: " + str(self.FL.getEncVelocity()))
        #self.Logger.printCurrents()
        #print("turn: " + str(turn)\
        #    + " mag: " + str(magnitude)\
        #    + " dir: " + str(direction))

if __name__ == "__main__":
    wpilib.run(MainRobot)

