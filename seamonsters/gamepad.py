__author__ = "jacobvanthoog" # based on code by zach steele

import wpilib
import math
import seamonsters.joystick

class Gamepad(seamonsters.joystick.JoystickBase):
    """
    An extended Joystick specifically designed for Logitech gamepads. Like
    seamonsters.joystick.JoystickUtils, it adds dead zones and changes positive
    x to direction 0. The gamepad mode switch MUST be at X!

    The Gamepad class has constants defined for the numbers of gamepad buttons.
    These include the colored A, B, X, and Y buttons; the left and right
    bumpers; the left and right triggers; the left and right joysticks when
    pressed; the Back and Start buttons; and the 4 d-pad buttons. The state
    of these buttons can be checked with
    ``gamepad.getRawButton(Gamepad.BUTTON_CONSTANT)``.
    
    For more of Gamepad's supported methods, see
    ``seamonsters.joystick.JoystickUtils``, and `wpilib.joystick
    <http://robotpy.readthedocs.io/en/latest/wpilib/Joystick.html>`_
    """
    
    A = 1
    B = 2
    X = 3
    Y = 4
    LB = 5
    RB = 6
    BACK = 7
    START = 8
    LJ = 9
    RJ = 10
    
    LT = 11
    RT = 12
    UP = 13
    DOWN = 14
    LEFT = 15
    RIGHT = 16

    
    def __init__(self, port):
        seamonsters.joystick.JoystickBase.__init__(self, port)
        self.deadZone = .08
        # invert axes
        self.xInv = False
        self.yInv = False

    def getDPad(self):
        """
        Return the currently pressed direction of the d-pad. -1 is not pressed.
        0 - 7 represents the directions starting at Up and moving clockwise.
        """
        pov = self.getPOV()
        if pov == -1:
            return -1
        return int(round(self.getPOV() / 45.0))
        
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
        return math.atan2(self.getRawLY(False), self.getRawLX(False))

    def getRDirection(self):
        """
        Get the direction of the right joystick. wpilib.Joystick's built-in
        getDirection() says 0 is positive y. This version uses positive x.
        """
        return math.atan2(self.getRawRY(False), self.getRawRX(False))
    
    def getLTrigger(self):
        """
        Get how far the left trigger is pressed, as a value from 0.0 to 1.0
        """
        return self.getRawAxis(2)

    def getRTrigger(self):
        """
        Get how far the right trigger is pressed, as a value from 0.0 to 1.0
        """
        return self.getRawAxis(3)

    def getButtonCount(self):
        # override for extra "buttons"
        return 16

    def getRawButton(self, button):
        if button == Gamepad.LT:
            return self.getLTrigger() > .5
        elif button == Gamepad.RT:
            return self.getRTrigger() > .5
        elif button == Gamepad.UP:
            dpad = self.getDPad()
            return dpad == 0 or dpad == 1 or dpad == 7
        elif button == Gamepad.RIGHT:
            dpad = self.getDPad()
            return dpad == 1 or dpad == 2 or dpad == 3
        elif button == Gamepad.DOWN:
            dpad = self.getDPad()
            return dpad == 3 or dpad == 4 or dpad == 5
        elif button == Gamepad.LEFT:
            dpad = self.getDPad()
            return dpad == 5 or dpad == 6 or dpad == 7
        else:
            return super().getRawButton(button)
    
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
    
