__author__ = 'Dawson'
import wpilib

class PIDTest(wpilib.IterativeRobot):

    def robotInit(self, talonPort):
        self.Talon = wpilib.CANTalon(talonPort)
        self.Talon.setPID(1,0,1,0)
        self.Talon.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        #self.Talon.changeControlMode(wpilib.CANTalon.ControlMode.Speed)

        self.goalPosition = self.Talon.getEncPosition()
        self.maxVelocity = 10

        self.Joystick= wpilib.Joystick(0)
        self.JoystickValues = [0,0,0,0]

        self.PIDNumber = 0
        self.loopCalls = 0
        self.buttonAllowedTime = 0

    def teleopInit(self):
        self.goalPosition = self.Talon.getEncPosition()
    
    # DO NOT CHANGE TELEOPPERIODIC, CHANGE DOALLELSE
    def teleopPeriodic(self):
        if (self.buttonAllowedTime <= self.loopCalls):
            if self.Joystick.getRawButton(4):
                self.PIDNumber += 1
                if self.PIDNumber > 3:
                    self.PIDNumber = 0
                self.buttonAllowedTime = self.loopCalls + 5
            elif self.Joystick.getRawButton(3):
                self.changePID(1.1)
                self.buttonAllowedTime = self.loopCalls + 5
            elif self.Joystick.getRawButton(2):
                self.changePID(1/1.1)
                self.buttonAllowedTime = self.loopCalls + 5

        self.doAllElse()

        self.printAll()

        #AT END
        self.loopCalls += 1
        if self.loopCalls >= 1000000:
            self.loopCalls = 0

    def doAllElse(self):
        if not (abs(self.goalPosition - self.Talon.getEncPosition()) > 4000):
            self.goalPosition += self.Joystick.getY() * -1 * self.maxVelocity
        self.Talon.set(self.goalPosition)
        #self.Talon.set(self.Joystick.getY() * 10)

    def printAll(self):
        for i in range(0,5):
            print()
        print("Selection Number: " + str(self.PIDNumber) \
                + "     P=0, I=1, D=2, F=3")
        print("P: " + str(self.Talon.getP()) \
           + " I: " + str(self.Talon.getI()) \
           + " D: " + str(self.Talon.getD()) \
           + " F: " + str(self.Talon.getF()))
        print("Speed: " + str(self.Talon.getEncVelocity()))
        #print("Position Actual: " + str(self.Talon.getPosition()))
        #print("Position   Goal: " + str(self.goalPosition))
        print("Time Until Button: " \
                + str(self.buttonAllowedTime - self.loopCalls))

    def changePID(self, number):
        if self.PIDNumber == 0:
            self.Talon.setP(self.Talon.getP() * number)
        elif self.PIDNumber == 1:
            self.Talon.setI(self.Talon.getI() * number)
        elif self.PIDNumber == 2:
            self.Talon.setD(self.Talon.getD() * number)
        elif self.PIDNumber == 3:
            self.Talon.setF(self.Talon.getF() * number)
