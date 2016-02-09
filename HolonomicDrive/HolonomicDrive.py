__author__ = 'Dawson'
import wpilib
import math
class HolonomicDrive():
#PLEASE READ:
#Right side driving forward is assumed to be +1
#Turning counter-clockwise is assumed to be +1
#Meet these requriements and THEN use invertDrive() if it is all backwards.

#Summary:
#Turn should be passed in as -Joystick.getX, most likely


    def __init__(self, fl, fr, bl, br):
        self.FL = fl
        self.FR = fr
        self.BL = bl
        self.BR = br
        self.stores = [0.0, 0.0, 0.0, 0.0]
        self.wheelOffset = math.pi / 4
        self.invert = 1
        self.maxVelocity = 2000

    #USE THESE FEW FUNCTIONS BELOW

    def driveVoltage(self, magnitude, direction, turn):
        self.ensureControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        self.calcWheels(magnitude, direction, turn)
        self.setWheels()
        #self.logCurrent()

    def driveSpeed(self, magnitude, direction, turn):
        self.ensureControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.calcWheels(magnitude, direction, turn)
        self.scaleToMax()
        self.setWheels()
        #self.logCurrent()

    def driveSpeedJeffMode(self, magnitude, direction, turn): #Increments position to mock speed mode
        self.ensureControlMode(wpilib.CANTalon.ControlMode.Position)
        self.calcWheels(magnitude, direction, turn)
        self.scaleToMaxJeffMode()
        self.setWheelsJeffMode()

    def invertDrive(self):
        self.invert *= -1

    def setWheelOffset(self, angleInRadians):
        self.wheelOffset = angleInRadians

    def setMaxVelocity(self, velocity):
        self.maxVelocity = velocity

    #DO NOT USE THESE FUNCTIONS

    def calcWheels(self, magnitude, direction, turn):
        self.stores = [0.0, 0.0, 0.0, 0.0]
        self.addStrafe(magnitude, direction)
        self.addTurn(turn)
        self.scaleNumbers()
        #self.setWheels()

    def addStrafe(self, magnitude, direction):
        if magnitude > 1.0:
            fixedMagnitude = 1.0
        else:
            fixedMagnitude = magnitude
        self.stores[0] += fixedMagnitude * (math.sin(direction + self.wheelOffset)) * -1 #FL
        #self.stores[0] += fixedMagnitude
        self.stores[1] += fixedMagnitude * (math.sin((direction - self.wheelOffset))) #FR
        self.stores[2] += fixedMagnitude * (math.sin((direction - self.wheelOffset))) * -1 #BL
        self.stores[3] += fixedMagnitude * (math.sin((direction + self.wheelOffset))) #FR

    def addTurn(self, turn):
        for i in range (0,4):
            self.stores[i] += turn

    def scaleNumbers(self):
        largest = max(self.stores)
        if largest > 1:
            for number in self.stores:
                number = number / largest

    def setWheels(self):
        self.FL.set(self.stores[0] * self.invert)
        self.FR.set(self.stores[1] * self.invert)
        self.BL.set(self.stores[2] * self.invert)
        self.BR.set(self.stores[3] * self.invert)
        #print(str(self.stores[0])+ "     "+str(self.stores[1]) + "     "+ str(self.stores[2])+ "     " + str(self.stores[3]))

    def setWheelsJeffMode(self):
        self.FL.set(self.FL.getEncPosition() + self.stores[0] * self.invert)
        self.FR.set(self.FR.getEncPosition() + self.stores[1] * self.invert)
        self.BL.set(self.BL.getEncPosition() + self.stores[2] * self.invert)
        self.BR.set(self.BR.getEncPosition() + self.stores[3] * self.invert)

    def scaleToMax(self):
        for i in range (0,4):
            self.stores[i] *= self.maxVelocity

    def scaleToMaxJeffMode(self):
        for i in range (0,4):
            self.stores[i] *= self.maxVelocity / 5.0

    def ensureControlMode(self, controlMode):
        if self.FL.getControlMode() == self.FR.getControlMode() == self.BL.getControlMode() == self.BR.getControlMode() == controlMode:
            return
        print("SETTING CONTROL MODE")
        self.FL.changeControlMode(controlMode)
        self.FR.changeControlMode(controlMode)
        self.BL.changeControlMode(controlMode)
        self.BR.changeControlMode(controlMode)

    def logCurrent(self):
        print("FL Current: " + str(self.FL.getOutputCurrent()))
        print("FR Current: " + str(self.FR.getOutputCurrent()))
        print("BL Current: " + str(self.BL.getOutputCurrent()))
        print("BR Current: " + str(self.BR.getOutputCurrent()))

