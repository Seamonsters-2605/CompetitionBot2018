import wpilib, math

__author__ = "jacobvanthoog"

# Joystick api reference:
# http://robotpy.readthedocs.org/en/latest/wpilib/Joystick.html

positionDeadZone = 0.05 # 5 percent
twistDeadZone = 0.05
zDeadZone = 0.05


def createJoystick(port):
    joystick = Joystick(port)
    return JoystickUtils(joystick)

class JoystickUtils:

    def __init__(self, joystick):
        self.Joy = joystick
        
        # initialize button array
        self.NumButtons = self.getButtonCount()
        self.CurrentButtonState = [False for i in range(0, self.NumButtons + 1)]
        self.PreviousButtonState = [False for i in range(0, self.NumButtons + 1)]
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
    
    # These methods check if various parts of the joystick are
    # in the dead-zone, and return a boolean value:
    
    def positionInDeadZone(self):
        return self.Joy.getMagnitude() < positionDeadZone

    def twistInDeadZone(self):
        return abs(self.Joy.getTwist()) < twistDeadZone

    def zInDeadZone(self):
        return abs(self.Joy.getZ()) < zDeadZone

    # These methods return 0 if the joystick is in the dead-zone:

    def getX(self):
        if self.positionInDeadZone():
            return 0
        return self.Joy.getX()

    def getY(self):
        if self.positionInDeadZone():
            return 0
        return self.Joy.getY()

    def getZ(self):
        if self.zInDeadZone():
            return 0
        return self.Joy.getZ()

    def getTwist(self):
        if self.twistInDeadZone():
            return 0
        return self.Joy.getTwist()

    def getMagnitude(self):
        if self.positionInDeadZone():
            return 0
        return self.Joy.getMagnitude()

    # These methods ignore the dead-zone:

    def getDirection(self):
        return self.Joy.getDirectionRadians()

    def getRawX(self):
        return self.Joy.getX()

    def getRawY(self):
        return self.Joy.getY()

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
    
    def getTrigger(self):
        return self.Joy.getTrigger()

    def getTop(self):
        return self.Joy.getTop()

    # Button events:

    def updateButtons(self):
        for i in range(2, self.NumButtons + 1):
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
