__author__ = "jacobvanthoog"

import wpilib, math
from NewArm.NewArmControl import Arm
from JoystickLib.Gamepad import Gamepad

class NewArm:
    # use JoystickLib.Gamepad!
    def __init__(self, gamepad, _can):
        self.can = _can
        self.Arm = Arm(self.can)
        self.Gamepad = gamepad
        self.Enabled = True
        self.ToggleWasPressed = False

    def update(self):
        #print("Encoder at", self.can.getPosition())
        if self.Enabled:
            self.Arm.update()
            value = 4000 * self.Gamepad.getLY()
            if value != 0:
                self.Arm.movePosition(value)
            if self.Gamepad.getRawButton(Gamepad.BACK):
                print("Arm position", self.Arm.getPosition())

        if self.Gamepad.getRawButton(Gamepad.LJ):
            if not self.ToggleWasPressed:
                self.ToggleWasPressed = True
                self.toggle()
        else:
            self.ToggleWasPressed = False

    def toggle(self):
        if self.Enabled:
            self.disable()
        else:
            self.enable()

    def enable(self):
        print("Arm enabled!")
        self.can.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.Enabled = True

    def disable(self):
        print("Arm disabled!")
        self.can.changeControlMode(wpilib.CANTalon.ControlMode.Voltage)
        self.can.set(0)
        self.Enabled = False