__author__ = "jacobvanthoog"

import wpilib, math
from NewArm.NewArmControl import Arm
from JoystickLib.Gamepad import Gamepad

class NewArm:
    # use JoystickLib.Gamepad!
    def __init__(self, Port):
        self.can = wpilib.CANTalon(7)
        self.Arm = Arm(self.can)
        self.Gamepad = Gamepad.Gamepad(port = Port)

    def update(self):
        print("Encoder at", self.can.getPosition())
        self.Arm.update()
        self.Arm.movePosition(4000 * self.Gamepad.getLY())
