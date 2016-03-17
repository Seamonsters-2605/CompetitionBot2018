__author__ = "jacobvanthoog"

import wpilib, math
from NewArm.NewArmControl import Arm
from JoystickLib.Gamepad import Gamepad

class NewArm:
    # use JoystickLib.Gamepad!
    def __init__(self, gamepad):
        can = wpilib.CANTalon(6)
        self.Arm = Arm(can)
        self.Gamepad = gamepad

    def update(self):
        if self.Gamepad.getRawButton(Gamepad.LB):
            self.Arm.update()
            self.Arm.movePosition(4000 * self.Gamepad.getLY())
