__author__ = 'jacobvanthoog'
import wpilib

# based off code in HolonomicDrive
class JeffMode:

    def __init__(self, talon):
        self.Talon = talon

        if not (self.Talon.getControlMode() == wpilib.CANTalon.ControlMode.Position):
            self.Talon.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.encoderTarget = self.Talon.getEncPosition() #zero encoder targets
        self.invert = 1 # can be 1 or -1
        self.maxVelocity = 80 * 5


    def set(self, magnitude): #Increments position to mock speed mode
        store = magnitude * self.maxVelocity
        if not abs(self.Talon.getEncPosition() - self.encoderTarget) > 250: #Started @ 1000
            self.encoderTarget += store * self.invert
        self.Talon.set(self.encoderTarget)
    
    def invert(self, enabled=True):
        self.invert = -1 if enabled else 1

    def setMaxVelocity(self, velocity):
        self.maxVelocity = velocity
