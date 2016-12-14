__author__ = 'Dawson'

import wpilib
from seamonsters.gamepad import Gamepad

class PIDTest(wpilib.IterativeRobot):

    def robotInit(self, talonPort, ticksPerRotation=4000, maxVelocity=10):
        self.talonPort = talonPort
        
        self.Talon = wpilib.CANTalon(talonPort)
        self.Talon.setPID(1,0,1,0)
        self.Talon.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        #self.Talon.changeControlMode(wpilib.CANTalon.ControlMode.Speed)

        self.goalPosition = self.Talon.getPosition()
        self.maxVelocity = maxVelocity
        self.ticksPerRotation = ticksPerRotation

        self.gamepad = Gamepad(0)

        self.adjustFactor = 1.0
        self.PIDNumber = 0

    def teleopInit(self):
        print("PID Adjustor")
        print("Hold RT and move the left joystick to change motor speed")
        print("Press Start and Back to toggle the selected value (P, I, D, F)")
        print("Press Left/Right to increase/decrease the adjust factor")
        print("Press Up/Down to increase/decrease the selected value")
        print()
        print("Using CANTalon:", self.talonPort)
        print("Currently adjusting: P")
        
        self.goalPosition = self.Talon.getPosition()
    
    def teleopPeriodic(self):
        self.gamepad.updateButtons()
        
        if self.gamepad.buttonPressed(Gamepad.START):
            self.PIDNumber += 1
            if self.PIDNumber > 3:
                self.PIDNumber = 0
            self._printAdjustedValue()
        if self.gamepad.buttonPressed(Gamepad.BACK):
            self.PIDNumber -= 1
            if self.PIDNumber < 0:
                self.PIDNumber = 3
            self._printAdjustedValue()
        
        if self.gamepad.buttonPressed(Gamepad.LEFT):
            self.adjustFactor /= 2.0
            self._printAdjustFactor()
        if self.gamepad.buttonPressed(Gamepad.RIGHT):
            self.adjustFactor *= 2.0
            self._printAdjustFactor()
        
        elif self.gamepad.buttonPressed(Gamepad.UP):
            self._changePID(self.adjustFactor)
            self._printValues()
        elif self.gamepad.buttonPressed(Gamepad.DOWN):
            self._changePID(-self.adjustFactor)
            self._printValues()

        if self.gamepad.getRawButton(Gamepad.RT):
            if not (abs(self.goalPosition - self.Talon.getPosition()) \
                    > self.ticksPerRotation):
                self.goalPosition += self.gamepad.getLY() * -1 \
                                     * self.maxVelocity
            self.Talon.set(self.goalPosition) 
            print("Speed: " + str(self.Talon.getEncVelocity()))
    
        
    def _changePID(self, number):
        if self.PIDNumber == 0:
            self.Talon.setP(self.Talon.getP() + number)
        elif self.PIDNumber == 1:
            self.Talon.setI(self.Talon.getI() + number)
        elif self.PIDNumber == 2:
            self.Talon.setD(self.Talon.getD() + number)
        elif self.PIDNumber == 3:
            self.Talon.setF(self.Talon.getF() + number)

    def _printAdjustedValue(self):
        print("Currently adjusting: ", end="")
        if self.PIDNumber == 0:
            print("P")
        elif self.PIDNumber == 1:
            print("I")
        elif self.PIDNumber == 2:
            print("D")
        elif self.PIDNumber == 3:
            print("F")

    def _printAdjustFactor(self):
        print("Factor:", self.adjustFactor)

    def _printValues(self):
        print("P: " + str(self.Talon.getP()) \
           + " I: " + str(self.Talon.getI()) \
           + " D: " + str(self.Talon.getD()) \
           + " F: " + str(self.Talon.getF()))
