import wpilib
import math
import seamonsters.joystick

__author__ = "jacobvanthoog" # based on code by zach steele

class Gamepad(seamonsters.joystick.JoystickBase):
    """
    An extended Joystick specifically designed for gamepads. Like
    seamonsters.joystick.JoystickUtils, it adds dead zones and changes positive
    x to direction 0.
    """
    # button definitions
    # example:
    # gamepad.getRawButton(Gamepad.LT)
    X = 3
    A = 1
    B = 2
    Y = 4
    LB = 5
    RB = 6
    LT = 11
    RT = 12
    BACK = 7
    START = 8
    LJ = 9
    RJ = 10

    def setDeadZone(self, value):
        """
        Set the deadzone of the position of both joysticks, on a scale of 0 to
        1. If the magnitude is within this range it will be reported as 0.
        Default value is 0.08 (8 percent).
        """
        self.deadZone = value
    
    def __init__(self, port):
        seamonsters.joystick.JoystickBase.__init__(self, port)
        self.deadZone = .08

    def inDeadZone(self, value):
        return abs(value) < self.deadZone
    
    def getLY(self, enableDeadZone = True):
        number = self.getRawAxis(0)
        if self.inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

    def getLX(self, enableDeadZone = True):
        number = self.getRawAxis(1)
        if self.inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

    def getRX(self, enableDeadZone = True):
        number = self.getRawAxis(4)
        if self.inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

    def getRY(self, enableDeadZone = True):
        number = self.getRawAxis(3)
        if self.inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

    def getRDirection(self):
        return math.atan2(self.getRY(False), -self.getRX(False)) \
            - (math.pi / 2)

    def getRMagnitude(self, enableDeadZone = True):
        number = math.sqrt(self.getRX(False)**2 + self.getRY(False)**2)
        if self.inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

    def getLDirection(self):
        return math.atan2(self.getLY(False), self.getLX(False)) \
            - (math.pi / 2)

    def getLMagnitude(self, enableDeadZone = True):
        number = math.sqrt(self.getLX(False)**2 + self.getLY(False)**2)
        if self.inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

