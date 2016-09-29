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

    
    def __init__(self, port):
        seamonsters.joystick.JoystickBase.__init__(self, port)
        self.deadZone = .08
        # invert axes
        self.xInv = False
        self.yInv = False
        
    def invertX(self, enabled=True):
        """
        Choose whether to invert the value of the x axis.
        """
        self.xInv = enabled

    def invertY(self, enabled=True):
        """
        Choose whether to invert the value of the y axis.
        """
        self.yInv = enabled
        
    def setDeadZone(self, value):
        """
        Set the deadzone of the position of both joysticks, on a scale of 0 to
        1. If the magnitude is within this range it will be reported as 0.
        Default value is 0.08 (8 percent).
        """
        self.deadZone = value

    def inDeadZone(self, value):
        """
        Check if a value between -1 and 1 is within the position deadzone.
        Return a boolean value.
        """
        return abs(value) < self.deadZone
        
    def rInDeadZone(self):
        """
        Check if the right joystick is in the deadzone. Return a boolean value.
        """
        return self.inDeadZone(self.getRawRMagnitude())
        
    def lInDeadZone(self):
        """
        Check if the left joystick is in the deadzone. Return a boolean value.
        """
        return self.inDeadZone(self.getRawLMagnitude())
    
    def getLX(self, enableDeadZone = True):
        """
        Get the x-axis of the left joystick. The dead zone is enabled by
        default; set enableDeadZone to False to disable it.
        """
        if self.lInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawLX()

    def getLY(self, enableDeadZone = True):
        """
        Get the x-axis of the left joystick. The dead zone is enabled by
        default; set enableDeadZone to False to disable it.
        """
        if self.lInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawLY()
        
    def getLMagnitude(self, enableDeadZone = True):
        """
        Get the magnitude of the left joystick. The dead zone is enabled by
        default; set enableDeadZone to False to disable it.
        """
        if self.lInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawLMagnitude()

    def getRX(self, enableDeadZone = True):
        """
        Get the y-axis of the right joystick. The dead zone is enabled by
        default; set enableDeadZone to False to disable it.
        """
        if self.rInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawRX()

    def getRY(self, enableDeadZone = True):
        """
        Get the y-axis of the right joystick. The dead zone is enabled by
        default; set enableDeadZone to False to disable it.
        """
        if self.rInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawRY()
        
    def getRMagnitude(self, enableDeadZone = True):
        """
        Get the magnitude of the right joystick. The dead zone is enabled by
        default; set enableDeadZone to False to disable it.
        """
        if self.rInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawRMagnitude()
        
    def getLDirection(self):
        """
        Get the direction of the left joystick. wpilib.Joystick's built-in
        getDirection() says 0 is positive y. This version uses positive x.
        """
        return math.atan2(self.getRawLY(False), self.getRawLX(False)) \
            - (math.pi / 2)

    def getRDirection(self):
        """
        Get the direction of the right joystick. wpilib.Joystick's built-in
        getDirection() says 0 is positive y. This version uses positive x.
        """
        return math.atan2(self.getRawRY(False), -self.getRawRX(False)) \
            - (math.pi / 2)
    
    
    
    def getRawLX(self, enableDeadZone = True):
        return self.getRawAxis(0) * (-1 if self.xInv else 1)
        
    def getRawLY(self, enableDeadZone = True):
       return -self.getRawAxis(1) * (-1 if self.yInv else 1)

    def getRawRX(self, enableDeadZone = True):
        return self.getRawAxis(4) * (-1 if self.xInv else 1)

    def getRawRY(self, enableDeadZone = True):
        return -self.getRawAxis(5) * (-1 if self.yInv else 1)
        
    def getRawLMagnitude(self, enableDeadZone = True):
        return math.sqrt(self.getRawLX(False)**2 + self.getRawLY(False)**2)

    def getRawRMagnitude(self, enableDeadZone = True):
        return math.sqrt(self.getRawRX(False)**2 + self.getRawRY(False)**2)
    
