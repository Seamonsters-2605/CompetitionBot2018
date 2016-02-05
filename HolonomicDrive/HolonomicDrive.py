__author__ = 'Dawson'
import wpilib
import math
class HolonomicDrive(wpilib.IterativeRobot):

    def __init__(self, fl, fr, bl, br):
        self.FL = fl
        self.FR = fr
        self.BL = bl
        self.BR = br
        self.stores = [0.0, 0.0, 0.0, 0.0]
        self.wheelOffset = math.pi / 4
        self.invert = 1
        self.maxVelocity = 1000

    #USE THESE FEW FUNCTIONS BELOW

    def driveVoltage(self, magnitude, direction, turn):
        self.ensureControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        self.calcWheels(magnitude, direction, turn)
        self.setWheels()
        self.logCurrent()

    def driveSpeed(self, magnitude, direction, turn):
        self.ensureControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.calcWheels(magnitude, direction, turn)
        self.scaleToMax()
        self.setWheels()
        self.logCurrent()

    def invert(self):
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
        self.setWheels()

    def addStrafe(self, magnitude, direction):
        if magnitude > 1.0:
            fixedMagnitude = 1.0
        else:
            fixedMagnitude = magnitude
        self.stores[0] += fixedMagnitude * (math.sin(direction + self.wheelOffset)) * -1 * self.invert #FL
        #self.stores[0] += fixedMagnitude
        self.stores[1] += fixedMagnitude * (math.sin((direction - self.wheelOffset))) * self.invert #FR
        self.stores[2] += fixedMagnitude * (math.sin((direction - self.wheelOffset))) * -1 * self.invert #BL
        self.stores[3] += fixedMagnitude * (math.sin((direction + self.wheelOffset))) * self.invert #FR

    def addTurn(self, turn):
        for i in range (0,4):
            self.stores[i] += turn * self.invert

    def scaleNumbers(self):
        largest = max(self.stores)
        if largest > 1:
            for number in self.stores:
                number = number / largest

    def setWheels(self):
        self.FL.set(self.stores[0])
        self.FR.set(self.stores[1])
        self.BL.set(self.stores[2])
        self.BR.set(self.stores[3])
        #print(str(self.stores[0])+ "     "+str(self.stores[1]) + "     "+ str(self.stores[2])+ "     " + str(self.stores[3]))


    def scaleToMax(self):
        for number in self.stores:
            number *= self.maxVelocity

    def ensureControlMode(self, controlMode):
        if self.FL.getControlMode() == controlMode:
            if self.FR.getControlMode() == controlMode:
                if self.BL.getControlMode() == controlMode:
                    if self.BR.getControlMode() == controlMode:
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

