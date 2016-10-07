__author__ = 'Dawson'

import wpilib
import seamonsters.joystick

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

        self.Joystick = seamonsters.joystick.JoystickUtils(0)
        self.JoystickValues = [0,0,0,0]

        self.PIDNumber = 0

    def teleopInit(self):
        print("PID Adjustor")
        print("Move the joystick up and down to spin the motor")
        print("Press 4 to toggle the selected value (P, I, D, F)")
        print("Use 2 and 3 to increase/decrease the selected value")
        print("Hold trigger to print the speed of the motor continuously")
        print()
        print("Using CANTalon:", self.talonPort)
        
        self.goalPosition = self.Talon.getPosition()
    
    # DO NOT CHANGE TELEOPPERIODIC, CHANGE DOALLELSE
    def teleopPeriodic(self):
        self.Joystick.updateButtons()
        
        if self.Joystick.buttonPressed(4):
            self.PIDNumber += 1
            if self.PIDNumber > 3:
                self.PIDNumber = 0
            print("Currently adjusting: ", end="")
            if self.PIDNumber == 0:
                print("P")
            elif self.PIDNumber == 1:
                print("I")
            elif self.PIDNumber == 2:
                print("D")
            elif self.PIDNumber == 3:
                print("F")
                    
        elif self.Joystick.buttonPressed(3):
            self.changePID(1.1)
            self.printValues()
        
        elif self.Joystick.buttonPressed(2):
            self.changePID(1.0/1.1)
            self.printValues()
        
        elif self.Joystick.getRawButton(1):
            print("Speed: " + str(self.Talon.getVelocity()))
        
        if not (abs(self.goalPosition - self.Talon.getPosition()) \
                > self.ticksPerRotation):
            self.goalPosition += self.Joystick.getY() * -1 * self.maxVelocity
        self.Talon.set(self.goalPosition)
        
        
    def printValues(self):
        print("P: " + str(self.Talon.getP()) \
           + " I: " + str(self.Talon.getI()) \
           + " D: " + str(self.Talon.getD()) \
           + " F: " + str(self.Talon.getF()))
        
    def changePID(self, number):
        if self.PIDNumber == 0:
            self.Talon.setP(self.Talon.getP() * number)
        elif self.PIDNumber == 1:
            self.Talon.setI(self.Talon.getI() * number)
        elif self.PIDNumber == 2:
            self.Talon.setD(self.Talon.getD() * number)
        elif self.PIDNumber == 3:
            self.Talon.setF(self.Talon.getF() * number)
