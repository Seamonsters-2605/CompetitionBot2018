__author__ = "jacobvanthoog"

import wpilib, math
from ArmReplay import ArmReplay
from ArmReplayReader import ArmReplayReader

class TestArmEncoders (wpilib.IterativeRobot):

    def robotInit(self):
        self.Arm1 = wpilib.CANTalon(0)
        self.Arm2 = wpilib.CANTalon(1)
        self.Arm2.reverseSensor(True)
        self.Control = ArmReplay(self.Arm1, self.Arm2)
        self.Joystick = wpilib.Joystick(0)
        self.Replay = ArmReplayReader(self.Control, "testPath.txt")

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        #print(self.Arm1.getEncPosition(), self.Arm2.getEncPosition())
        if self.Joystick.getRawButton(1): #A
            self.Control.setTarget(self.Control.getPositions())
        if self.Joystick.getRawButton(2): #B
            self.Control.update()
        if self.Joystick.getRawButton(3): #X
            self.Replay.enable()
        if self.Joystick.getRawButton(4): #Y
            self.Replay.disable()
        self.Replay.update()

if __name__ == "__main__":
    wpilib.run(TestArmEncoders)
