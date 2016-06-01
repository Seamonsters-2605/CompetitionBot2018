import wpilib
import math
import seamonsters.joystick

__author__ = "jacobvanthoog" # based on code by zach steele

class Gamepad(seamonsters.joystick.JoystickBase):
    """
    An extended Joystick specifically designed for Logitech gamepads. Like
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
        
    def rInDeadZone(self):
        return self.inDeadZone(self.getRawRMagnitude())
        
    def lInDeadZone(self):
        return self.inDeadZone(self.getRawLMagnitude())
    
    def getLX(self, enableDeadZone = True):
        if self.lInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawLX()

    def getLY(self, enableDeadZone = True):
        if self.lInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawLY()
        
    def getLMagnitude(self, enableDeadZone = True):
        if self.lInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawLMagnitude()

    def getRX(self, enableDeadZone = True):
        if self.rInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawRX()

    def getRY(self, enableDeadZone = True):
        if self.rInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawRY()
        
    def getRMagnitude(self, enableDeadZone = True):
        if self.rInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawRMagnitude()
        
    def getLDirection(self):
        return math.atan2(self.getRawLY(False), self.getRawLX(False)) \
            - (math.pi / 2)

    def getRDirection(self):
        return math.atan2(self.getRawRY(False), -self.getRawRX(False)) \
            - (math.pi / 2)
    
    
    
    def getRawLX(self, enableDeadZone = True):
        return self.getRawAxis(1)
        
    def getRawLY(self, enableDeadZone = True):
       return self.getRawAxis(0)

    def getRawRX(self, enableDeadZone = True):
        return self.getRawAxis(4)

    def getRawRY(self, enableDeadZone = True):
        return self.getRawAxis(3)
        
    def getRawLMagnitude(self, enableDeadZone = True):
        return math.sqrt(self.getLX(False)**2 + self.getLY(False)**2)

    def getRawRMagnitude(self, enableDeadZone = True):
        return math.sqrt(self.getRawRX(False)**2 + self.getRawRY(False)**2)
    