import math
from wpilib.buttons import JoystickButton
from wpilib import Joystick

__author__ = "jacobvanthoog"

# Joystick api reference:
# http://robotpy.readthedocs.org/en/latest/wpilib/Joystick.html


class JoystickBase(Joystick):
    
    def __init__(self, port):
        Joystick.__init__(self, port)
        # initialize button array
        self.NumButtons = self.getButtonCount()
        self.CurrentButtonState = [False for i in range(0, self.NumButtons + 1)]
        self.PreviousButtonState= [False for i in range(0, self.NumButtons + 1)]
        self.updateButtons()
    
    def getJoystickButton(self, buttonNumber):
        return JoystickButton(self, buttonNumber)

    def updateButtons(self):
        for i in range(1, self.NumButtons + 1):
            self.PreviousButtonState[i] = self.CurrentButtonState[i]
            self.CurrentButtonState[i] = self.getRawButton(i)

    def buttonPressed(self, b):
        return self.CurrentButtonState[b] and (not self.PreviousButtonState[b])

    def buttonReleased(self, b):
        return (not self.CurrentButtonState[b]) and self.PreviousButtonState[b]
        

class JoystickUtils(JoystickBase):

    def __init__(self, port):
        JoystickBase.__init__(self, port)
        self.XInv = False
        self.YInv = False

        self.positionDeadZone = 0.05 # 5 percent
        self.twistDeadZone = 0.1
        self.zDeadZone = 0.1
        

    # Whether to invert the x or y axis

    def invertX(self, enabled=True):
        self.XInv = enabled

    def invertY(self, enabled=True):
        self.YInv = enabled

    # Set deadzones

    def setPositionDeadZone(self, value):
        self.positionDeadZone = value

    def setTwistDeadZone(self, value):
        self.twistDeadZone = value

    def setZDeadZone(self, value):
        self.zDeadZone = value
    
    # These methods check if various parts of the joystick are
    # in the dead-zone, and return a boolean value:
    
    def positionInDeadZone(self):
        return self.getRawMagnitude() < self.positionDeadZone

    def twistInDeadZone(self):
        return abs(self.getRawTwist()) < self.twistDeadZone

    def zInDeadZone(self):
        return abs(self.getRawZ()) < self.zDeadZone

    # These methods return 0 if the joystick is in the dead-zone:

    def getX(self, enableDeadZone = True):
        if self.positionInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawX()

    def getY(self, enableDeadZone = True):
        if self.positionInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawY()

    def getZ(self, enableDeadZone = True):
        if self.zInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawZ()

    def getTwist(self, enableDeadZone = True):
        if self.twistInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawTwist()

    def getMagnitude(self, enableDeadZone = True):
        if self.positionInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawMagnitude()

    def getDirection(self):
        # Joystick's built-in getDirection() says 0 is positive y
        # It should be positive x
        return math.atan2(self.getRawY(), self.getRawX())

    # These methods ignore the dead-zone, but they do invert the axis if that
    # is enabled. Calling the above methods with enableDeadZone=False is
    # preferred.

    def getRawX(self):
        x = Joystick.getX(self)
        return -x if self.XInv else x

    def getRawY(self):
        y = Joystick.getY(self)
        return -y if self.YInv else y

    def getRawZ(self):
        return Joystick.getZ(self)

    def getRawTwist(self):
        return Joystick.getTwist(self)

    def getRawMagnitude(self):
        return Joystick.getMagnitude(self)
    
    def getRawAxis(self, axis):
        return Joystick.getRawAxis(self, axis)
    
    
    
