__author__ = "jacobvanthoog"

import math
import wpilib
import JoystickLib.joystickLib
from HolonomicDrive.HolonomicDrive import HolonomicDrive

class MainRobot (wpilib.IterativeRobot):

    def robotInit(self):
        self.FL = wpilib.CANTalon(2)
        self.FR = wpilib.CANTalon(2)
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

        self.MoveJoy = joystickLib.createJoystick(0)
        self.MoveJoy.invertY()
        self.TurnJoy = joystickLib.createJoystick(1)
        self.TurnJoy.invertY()

        self.Drive = HolonomicDrive(self.FL, self.FR, self.BL, self.BR)
        self.Drive.invertDrive(True)
        self.Drive.setWheelOffset(math.radians(27))
        self.Drive.setDriveMode(HolonomicDrive.DriveMode.JEFF)
        
        

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.Drive.zeroEncoderTargets()

    def teleopPeriodic(self):
        turn = -self.TurnJoy.getX()
        magnitude = self.MoveJoy.getMagnitude()
        direction = self.MoveJoy.getDirection()
        self.Drive.drive(magnitude, direction, turn)



if __name__ == "__main__":
    wpilib.run(MainRobot)

