import wpilib
import math
import seamonsters.joystick

__author__ = "jacobvanthoog" # based on code by zach steele

class Gamepad(seamonsters.joystick.JoystickBase):
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
        self.deadZone = value
    
    def __init__(self, port):
        seamonsters.joystick.JoystickBase.__init__(self, port)
        self.deadZone = .08

    def inDeadZone(self, value):
        return abs(value) < self.deadZone
    
    def getLY(self, enableDeadZone = True):
        number = self.getRawAxis(0)
        if inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

    def getLX(self, enableDeadZone = True):
        number = self.getRawAxis(1)
        if inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

    def getRX(self, enableDeadZone = True):
        number = self.getRawAxis(4)
        if inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

    def getRY(self, enableDeadZone = True):
        number = self.getRawAxis(3)
        if inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

    def getRDirection(self):
        return math.atan2(self.getRY(False), -self.getRX(False)) \
            - (math.pi / 2)

    def getRMagnitude(self, enableDeadZone = True):
        number = math.sqrt(self.getRX(False)**2 + self.getRY(False)**2)
        if inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

    def getLDirection(self):
        return math.atan2(self.getLY(False), self.getLX(False)) \
            - (math.pi / 2)

    def getLMagnitude(self, enableDeadZone = True):
        number = math.sqrt(self.getLX(False)**2 + self.getLY(False)**2)
        if inDeadZone(number) and enableDeadZone:
            return 0.0
        return number

