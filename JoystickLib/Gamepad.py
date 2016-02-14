import wpilib
import math
def createGamepad(port):
    gamepad = wpilib.Joystick(port)
    return Gamepad(gamepad)

class Gamepad(wpilib.Joystick):
    def __init__(self, port):
        super(Gamepad, self).__init__(port = port)
        deadzone = .08


    def getButtonByLetter(self, string):
        if string == "X":
            return self.getRawButton(1)
        if string == "A":
            return self.getRawButton(2)
        if string == "B":
            return self.getRawButton(3)
        if string == "Y":
            return self.getRawButton(4)
        if string == "LB":
            return self.getRawButton(5)
        if string == "RB":
            return self.getRawButton(6)
        if string == "LT":
            return self.getRawButton(7)
        if string == "RT":
            return self.getRawButton(8)
        if string == "Back":
            return self.getRawButton(9)
        if string == "Start":
            return self.getRawButton(10)
        if string == "LJ":
            return self.getRawButton(11)
        if string == "RJ":
            return self.getRawButton(12)
        return False
    def getLY(self):
        return self.getRawAxis(0)
    def getLX(self):
        return self.getRawAxis(1)
    def getRX(self):
        return self.getRawAxis(4)
    def getRY(self):
        return self.getRawAxis(3)
    def getRDirection(self):
        return math.atan2(self.getRawAxis(3), self.getRawAxis(4)) + (math.pi/180 * 90)
    def getRMagnitude(self):
        return math.sqrt((self.getRawAxis(3) * self.getRawAxis(3)) +
                         (self.getRawAxis(4) * self.getRawAxis(4)))
    def getLDirection(self):
        return math.atan2(self.getRawAxis(0), self.getRawAxis(1)) + (math.pi/180 * 90)
    def getLMagnitude(self):
        return math.sqrt((self.getRawAxis(0) * self.getRawAxis(0)) +
                         (self.getRawAxis(1) * self.getRawAxis(1)))
