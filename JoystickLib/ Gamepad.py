import wpilib
import math

class Gamepad():
    def __init__(self, port):
        self.gamepad = wpilib.Joystick(port)
        self.deadzone = .08
    def getButtonByLetter(self, string):
        if string == "X":
            return self.gamepad.getRawButton(1)
        if string == "A":
            return self.gamepad.getRawButton(2)
        if string == "B":
            return self.gamepad.getRawButton(3)
        if string == "Y":
            return self.gamepad.getRawButton(4)
        if string == "LB":
            return self.gamepad.getRawButton(5)
        if string == "RB":
            return self.gamepad.getRawButton(6)
        if string == "LT":
            return self.gamepad.getRawButton(7)
        if string == "RT":
            return self.gamepad.getRawButton(8)
        if string == "Back":
            return self.gamepad.getRawButton(9)
        if string == "Start":
            return self.gamepad.getRawButton(10)
        if string == "LJ":
            return self.gamepad.getRawButton(11)
        if string == "RJ":
            return self.gamepad.getRawButton(12)
    def getLY(self):
        return self.gamepad.getRawAxis(0)
    def getLX(self):
        return self.gamepad.getRawAxis(1)
    def getRX(self):
        return self.gamepad.getRawAxis(4)
    def getRY(self):
        return self.gamepad.getRawAxis(3)
    def getRDirection(self):
        return math.atan2(self.gamepad.getRawAxis(3), self.gamepad.getRawAxis(4)) + (math.pi/180 * 90)
    def getRMagnitude(self):
         return math.sqrt((self.gamepad.getRawAxis(3) * self.gamepad.getRawAxis(3)) +
                         (self.gamepad.getRawAxis(4) * self.gamepad.getRawAxis(4))
    def getLDirection(self):
        return math.atan2(self.gamepad.getRawAxis(0), self.gamepad.getRawAxis(1)) + (math.pi/180 * 90)
    def getLMagnitude(self):
        return math.sqrt((self.gamepad.getRawAxis(0) * self.gamepad.getRawAxis(0)) +
                         (self.gamepad.getRawAxis(1) * self.gamepad.getRawAxis(1)))
