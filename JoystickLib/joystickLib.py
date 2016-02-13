import wpilib, math
from wpilib.buttons import JoystickButton

__author__ = "jacobvanthoog"

# Joystick api reference:
# http://robotpy.readthedocs.org/en/latest/wpilib/Joystick.html

positionDeadZone = 0.05 # 5 percent
twistDeadZone = 0.1
zDeadZone = 0.1


def createJoystick(port):
    joystick = wpilib.Joystick(port)
    return JoystickUtils(joystick)

class JoystickUtils:

    def __init__(self, joystick):
        self.Joy = joystick

        self.XInv = False
        self.YInv = False
        
        # initialize button array
        self.NumButtons = self.getButtonCount()
        self.CurrentButtonState = [False for i in range(0, self.NumButtons + 1)]
        self.PreviousButtonState= [False for i in range(0, self.NumButtons + 1)]
        self.updateButtons()
    
    def getJoystick(self):
        return self.Joy

    def getName(self):
        return self.Joy.getName()

    def getType(self):
        return self.Joy.getType()

    def setOutput(self, outputNumber, value):
        return self.Joy.setOutput(outputNumber, value)

    def setOutputs(self, value):
        return self.Joy.setOutputs(value)

    def flushOutputs(self):
        return self.Joy.flushOutputs()

    # Whether to invert the x or y axis

    def invertX(self, enabled=True):
        self.XInv = enabled

    def invertY(self, enabled=True):
        self.YInv = enabled
    
    # These methods check if various parts of the joystick are
    # in the dead-zone, and return a boolean value:
    
    def positionInDeadZone(self):
        return self.getRawMagnitude() < positionDeadZone

    def twistInDeadZone(self):
        return abs(self.getRawTwist()) < twistDeadZone

    def zInDeadZone(self):
        return abs(self.getRawZ()) < zDeadZone

    # These methods return 0 if the joystick is in the dead-zone:

    def getX(self):
        if self.positionInDeadZone():
            return 0
        return self.getRawX()

    def getY(self):
        if self.positionInDeadZone():
            return 0
        return self.getRawY()

    def getZ(self):
        if self.zInDeadZone():
            return 0
        return self.getRawZ()

    def getTwist(self):
        if self.twistInDeadZone():
            return 0
        return self.getRawTwist()

    def getMagnitude(self):
        if self.positionInDeadZone():
            return 0
        return self.getRawMagnitude()

    def getDirection(self):
        # Joystick's built-in getDirection() says 0 is positive y
        # It should be positive x
        return math.atan2(self.getRawY(), self.getRawX())

    # These methods ignore the dead-zone, but they do invert the axis if that
    # is enabled:

    def getRawX(self):
        x = self.Joy.getX()
        return -x if self.XInv else x

    def getRawY(self):
        y = self.Joy.getY()
        return -y if self.YInv else y

    def getRawZ(self):
        return self.Joy.getZ()

    def getRawTwist(self):
        return self.Joy.getTwist()

    def getRawMagnitude(self):
        return self.Joy.getMagnitude()
    
    def getRawAxis(self, axis):
        return self.Joy.getRawAxis(axis)
    
    # Buttons:
    
    def getButtonCount(self):
        return self.Joy.getButtonCount()

    def getButton(self, buttonType):
        return self.Joy.getButton(buttonType);

    def getRawButton(self, buttonNumber):
        return self.Joy.getRawButton(buttonNumber)
    
    def getJoystickButton(self, buttonNumber):
        return JoystickButton(self.getJoystick(), buttonNumber)
    
    def getTrigger(self):
        return self.Joy.getTrigger()

    def getTop(self):
        return self.Joy.getTop()

    # Button events:

    def updateButtons(self):
        for i in range(1, self.NumButtons + 1):
            self.PreviousButtonState[i] = self.CurrentButtonState[i]
            self.CurrentButtonState[i] = self.getRawButton(i)

    def buttonPressed(self, b):
        return self.CurrentButtonState[b] and (not self.PreviousButtonState[b])

    def buttonReleased(self, b):
        return (not self.CurrentButtonState[b]) and self.PreviousButtonState[b]

    
    def getPOVCount(self):
        return self.Joy.getPOVCount()
    
    def getPOV(self, pov=0):
        return self.Joy.getPOV(pov)
    
    
    def getThrottle(self):
        return self.Joy.getThrottle()
    
    def setRumble(self, rumbleType, value):
        return self.Joy.setRumble(rumbleType, value)
