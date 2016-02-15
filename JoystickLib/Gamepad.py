import wpilib
import math
def createGamepad(port):
    gamepad = wpilib.Joystick(port)
    return Gamepad(gamepad)

class Gamepad(wpilib.Joystick):
    #button definitions
    # example:
    # gamepad.getRawButton(Gamepad.LT)
    X = 1
    A = 2
    B = 3
    Y = 4
    LB = 5
    RB = 6
    LT = 7
    RT = 8
    BACK = 9
    START = 10
    LJ = 11
    RJ = 12
    
    def __init__(self, port):
        super(Gamepad, self).__init__(port = port)
        self.deadzone = .08
        self.isDeadzoneActive = True
    
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
        number = self.getRawAxis(0)
        if self.isDeadzoneActive:
            if abs(number) < self.deadzone:
                return 0.0
        return number
    def getLX(self):
        number = self.getRawAxis(1)
        print("LX: " + str(number))
        if self.isDeadzoneActive:
            if abs(number) < self.deadzone:
                return 0.0
        return number
    def getRX(self):
        number = self.getRawAxis(4)
        if self.isDeadzoneActive:
            if abs(number) < self.deadzone:
                return 0.0
        return number
    def getRY(self):
        number = self.getRawAxis(3)
        if self.isDeadzoneActive:
            if abs(number) < self.deadzone:
                return 0.0
        return number
    def getRDirection(self):
        return math.atan2(self.getRawAxis(3), -self.getRawAxis(4)) - (math.pi/180 * 90)
    def getRMagnitude(self):
        number = math.sqrt((self.getRawAxis(3) * self.getRawAxis(3)) +
                         (self.getRawAxis(4) * self.getRawAxis(4)))
        if self.isDeadzoneActive:
            if number < self.deadzone:
                return 0.0
        return number
    def getLDirection(self):
        return math.atan2(self.getRawAxis(0), self.getRawAxis(1)) - (math.pi/180 * 90)
    def getLMagnitude(self):
        number = math.sqrt((self.getRawAxis(0) * self.getRawAxis(0)) +
                         (self.getRawAxis(1) * self.getRawAxis(1)))
        if self.isDeadzoneActive:
            if number < self.deadzone:
                return 0.0
        return number

    def setIsDeadzoneActive(self, bool):
        self.isDeadzoneActive = bool

    def setDeadzone(self, inDeadzone):
        self.deadzone = inDeadzone
