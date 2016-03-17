__author__ = "jacobvanthoog"

POS_1 = 0
POS_2 = 0
POS_3 = 0
POS_4 = 0

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
        self.Arm.update()
        if self.Gamepad.getRawButton(Gamepad.BACK):
           print("Arm pos.", self.Arm.getPosition())
        
        value = 4000 * self.Gamepad.getLY()
        if not value == 0:
           self.Arm.movePosition(value)

        if self.Gamepad.getRawButton(Gamepad.LJ):
            self.Arm.movePosition(0)
            
        # get POV direction
        pov = self.Gamepad.getPOV()
        if not pov == -1: #if POV is pressed
            pov = round(pov / 90)
            if pov == 0 or pov == 4: # could round up
                self.Arm.setTarget(POS_1)
            elif pov == 1:
                self.Arm.setTarget(POS_2)
            elif pov == 2:
                self.Arm.setTarget(POS_3)
            elif pov == 3:
                self.Arm.setTarget(POS_4)
