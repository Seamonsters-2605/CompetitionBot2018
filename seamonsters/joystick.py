import math
from wpilib.buttons import JoystickButton
from wpilib import Joystick

__author__ = "jacobvanthoog"

# Joystick api reference:
# http://robotpy.readthedocs.org/en/latest/wpilib/Joystick.html


class JoystickBase(Joystick):
    """
    The base for other joystick utilities classes. This has methods for checking
    whether buttons have been pressed or released.
    """
    def __init__(self, port):
        super().__init__(port)
        # initialize button array
        self.NumButtons = self.getButtonCount()
        if self.NumButtons == 0:
            print("WARNING: Joystick has 0 buttons! Defaulting to 16")
            self.NumButtons = 16
        self.CurrentButtonState = [False] * (self.NumButtons + 1)
        self.PreviousButtonState= [False] * (self.NumButtons + 1)
        self.updateButtons()
    
    def getJoystickButton(self, buttonNumber):
        return JoystickButton(self, buttonNumber)

    def updateButtons(self):
        """
        Update the current state of the buttons. Call this in the main loop.
        """
        for i in range(1, self.NumButtons + 1):
            self.PreviousButtonState[i] = self.CurrentButtonState[i]
            self.CurrentButtonState[i] = self.getRawButton(i)

    def buttonPressed(self, b):
        """
        Check if the specified button was pressed between the most recent 
        updateButtons() call and the call before that.
        """
        return self.CurrentButtonState[b] and (not self.PreviousButtonState[b])

    def buttonReleased(self, b):
        """
        Check if the specified button was released between the most recent 
        updateButtons() call and the call before that.
        """
        return (not self.CurrentButtonState[b]) and self.PreviousButtonState[b]
        

class JoystickUtils(JoystickBase):
    """
    An extended Joystick with extra utilities for deadzones and a new definition
    of direction: positive X is now zero, which is more standard.
    """
    def __init__(self, port):
        super().__init__(port)
        self.XInv = False
        self.YInv = False

        self.positionDeadZone = 0.05 # 5 percent
        self.twistDeadZone = 0.1
        self.zDeadZone = 0.1
    

    def invertX(self, enabled=True):
        """
        Choose whether to invert the value of the x axis.
        """
        self.XInv = enabled

    def invertY(self, enabled=True):
        """
        Choose whether to invert the value of the y axis.
        """
        self.YInv = enabled
    

    def setPositionDeadZone(self, value):
        """
        Set the deadzone of the position of the joystick, on a scale of 0 to 1.
        If the magnitude is within this range it will be reported as 0. Default
        value is 0.05 (5 percent).
        """
        self.positionDeadZone = value

    def setTwistDeadZone(self, value):
        """
        Set the deadzone of the twist of the joystick, on a scale of 0 to 1.
        If the twist is within this range it will be reported as 0. Default
        value is 0.1 (10 percent).
        """
        self.twistDeadZone = value

    def setZDeadZone(self, value):
        """
        Set the deadzone of the z-axis of the joystick, on a scale of 0 to 1.
        If the value is within this range it will be reported as 0. Default
        value is 0.1 (10 percent).
        """
        self.zDeadZone = value
    
    
    def positionInDeadZone(self):
        """
        Check if the position of the joystick is currently in the deadzone.
        Return a boolean value.
        """
        return self.getRawMagnitude() < self.positionDeadZone

    def twistInDeadZone(self):
        """
        Check if the twist of the joystick is currently in the deadzone.
        Return a boolean value.
        """
        return abs(self.getRawTwist()) < self.twistDeadZone

    def zInDeadZone(self):
        """
        Check if the z-axis of the joystick is currently in the deadzone.
        Return a boolean value.
        """
        return abs(self.getRawZ()) < self.zDeadZone

    # These methods return 0 if the joystick is in the dead-zone:

    def getX(self, enableDeadZone = True):
        """
        Get the value of the x-axis. The dead zone is enabled by default; set
        enableDeadZone to False to disable it.
        """
        if self.positionInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawX()

    def getY(self, enableDeadZone = True):
        """
        Get the value of the y-axis. The dead zone is enabled by default; set
        enableDeadZone to False to disable it.
        """
        if self.positionInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawY()

    def getZ(self, enableDeadZone = True):
        """
        Get the value of the z-axis. The dead zone is enabled by default; set
        enableDeadZone to False to disable it.
        """
        if self.zInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawZ()

    def getTwist(self, enableDeadZone = True):
        """
        Get the twist of the joystick. The dead zone is enabled by default; set
        enableDeadZone to False to disable it.
        """
        if self.twistInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawTwist()

    def getMagnitude(self, enableDeadZone = True):
        """
        Get the magnitude of the joystick. The dead zone is enabled by default;
        set enableDeadZone to False to disable it.
        """
        if self.positionInDeadZone() and enableDeadZone:
            return 0.0
        return self.getRawMagnitude()

    def getDirection(self):
        """
        Get the direction of the joystick. wpilib.Joystick's built-in
        getDirection() says 0 is positive y. This version uses positive x.
        """
        return math.atan2(self.getRawY(), self.getRawX())

    # These methods ignore the dead-zone, but they do invert the axis if that
    # is enabled. Calling the above methods with enableDeadZone=False is
    # preferred.

    def getRawX(self):
        x = super().getX()
        return -x if self.XInv else x

    def getRawY(self):
        y = super().getY()
        return -y if self.YInv else y

    def getRawZ(self):
        return super().getZ()

    def getRawTwist(self):
        return super().getTwist()

    def getRawMagnitude(self):
        return math.sqrt(self.getRawX()**2 + self.getRawY()**2)

class DynamicAxis:

    # try 2.0, 4.0, 0.5?
    def __init__(self, exponent=1.0, speedScaleFactor=0.0,
                 speedScaleExponent=0.0, deadZone=None):
        """
        ``exponent`` should be >= 1. ``speedScaleFactor`` should be >= 1.
        ``speedScaleExponent`` should be <= 1 (use 0 to ignore speed).
        ``deadZone`` should be < 1 and close to 0.
        """
        self.exponent = exponent
        self.speedScaleFactor = speedScaleFactor
        self.speedScaleExponent = speedScaleExponent
        self.deadZone = deadZone
        
        self.values = [0.0, 0.0, 0.0]
        self.scale = 1.0

    def update(self, value):
        if self.deadZone is not None:
            if abs(value) < self.deadZone:
                value = 0.0
        self.values.append(value)
        self.values.pop(0)
        
        reversedValues = list(self.values)
        reversedValues.reverse()
        if 0.0 in reversedValues:
            if reversedValues.index(0) == len(reversedValues) - 1:
                self.scale = (abs(self.values[-1]) * self.speedScaleFactor) \
                    ** self.speedScaleExponent
        
        adjustedValue = (value * self.scale) ** self.exponent
        if value >= 0:
            adjustedValue = abs(adjustedValue)
        else:
            adjustedValue = -abs(adjustedValue)
        return adjustedValue

if __name__ == "__main__":
    axis = DynamicAxis()
    print(axis.update(0.0))
    print(axis.update(1.0))
    print(axis.update(1.0))
    print(axis.update(0.5))

