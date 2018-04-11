import wpilib

__author__ = "seamonsters"

def deadZone(value, deadZone = 0.08):
   if abs(value) < deadZone:
       return 0.0
   return value

def whileButtonPressed(joystick, button):
    """
    A generator which runs while the joystick button is pressed, then exits.
    :param joystick: a ``wpilib.Joystick``
    :param button: a button number
    """
    yield
    while joystick.getRawButton(button):
        yield

def untilButtonPressed(joystick, button):
    """
    A generator which runs until the joystick button is pressed, then exits.
    :param joystick: a ``wpilib.Joystick``
    :param button: a button number
    """
    yield
    while not joystick.getRawButton(button):
        yield

class DynamicAxis:
    """
    Makes values from a joystick axis go higher if you push them faster.
    """

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
        """
        Update the value of the axis
        :param value: the raw axis value from the joystick
        :return: the adjusted value
        """
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

