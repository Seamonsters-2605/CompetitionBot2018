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
    
    class DriveMode:
        VOLTAGE = 1
        SPEED = 2
        JEFF = 3

    def __init__(self, fl, fr, bl, br):
        self.FL = fl
        self.FR = fr
        self.BL = bl
        self.BR = br
        self.FL.setPID(1.0, 0.0, 3.0, 0.0)
        self.FR.setPID(1.0, 0.0, 3.0, 0.0)
        self.BL.setPID(1.0, 0.0, 3.0, 0.0)
        self.BR.setPID(1.0, 0.0, 3.0, 0.0)

        self.stores = [0.0, 0.0, 0.0, 0.0]
        self.encoderTargets = [0.0, 0.0, 0.0, 0.0]
        self.wheelOffset = math.pi / 4
        self.invert = 1 # can be 1 or -1
        self.maxVelocity = 80 * 5 #MAX VELOCITY IS FOR JEFF MODE (AKA INTEGRAL VELOCITY) AND IS MODIFIED FOR VELOCITY MODE
        self.slowModeMaxVelocity = 50
        self.previousDriveMode = HolonomicDrive.DriveMode.VOLTAGE
        self.driveMode = HolonomicDrive.DriveMode.VOLTAGE

    #USE THESE FEW FUNCTIONS BELOW


    # use the variables DriveMode.VOLTAGE, DriveMode.SPEED, etc. in this function
    # and NOT their values (1, 2, ...) -- those could change in the future
    def setDriveMode(self, mode):
        self.driveMode = mode

    def getDriveMode(self):
        return self.driveMode

    # a generic drive() function that calls the corresponding driveVoltage(),
    # driveSpeed(), etc. based on what the current driveMode is.
    def drive(self, magnitude, direction, turn):
        if self.driveMode == HolonomicDrive.DriveMode.VOLTAGE:
            self.driveVoltage(magnitude, direction, turn)
        elif self.driveMode == HolonomicDrive.DriveMode.SPEED:
            self.driveSpeed(magnitude, direction, turn)
        elif self.driveMode == HolonomicDrive.DriveMode.JEFF:
            self.driveSpeedJeffMode(magnitude, direction, turn)
    

    # these functions ignore the current driveMode setting
    
    def driveVoltage(self, magnitude, direction, turn):
        self.ensureControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        self.calcWheels(magnitude, direction, turn)
        self.setWheels()
        self.previousDriveMode = HolonomicDrive.DriveMode.VOLTAGE
        #self.logCurrent()

    def driveSpeed(self, magnitude, direction, turn):
        self.ensureControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.calcWheels(magnitude, direction, turn)
        self.scaleToMax()
        self.setWheels()
        self.previousDriveMode = HolonomicDrive.DriveMode.SPEED
        #self.logCurrent()

    def driveSpeedJeffMode(self, magnitude, direction, turn, slowmode = False): #Increments position to mock speed mode
        # if (turn == 0 and magnitude == 0):
        #     self.disableTalons()
        # elif self.FL.getControlMode() == wpilib.CANTalon.ControlMode.Disabled and\
        #      self.FR.getControlMode() == wpilib.CANTalon.ControlMode.Disabled and\
        #      self.BL.getControlMode() == wpilib.CANTalon.ControlMode.Disabled and\
        #      self.BR.getControlMode() == wpilib.CANTalon.ControlMode.Disabled:
        #     self.enableTalons()
        #     self.zeroEncoderTargets()
        self.ensureControlMode(wpilib.CANTalon.ControlMode.Position)
        if not self.previousDriveMode == 3:
            self.zeroEncoderTargets()
        self.calcWheels(magnitude, direction, turn)
        if slowmode:

            self.FL.setPID(12.0, 0.0, 40.0, 0.0)
            self.FR.setPID(12.0, 0.0, 40.0, 0.0)
            self.BL.setPID(12.0, 0.0, 40.0, 0.0)
            self.BR.setPID(12.0, 0.0, 40.0, 0.0)
            self.scaleToMaxJeffModeSlowMode()
        else:
            self.FL.setPID(1.0, 0.0, 3.0, 0.0)
            self.FR.setPID(1.0, 0.0, 3.0, 0.0)
            self.BL.setPID(1.0, 0.0, 3.0, 0.0)
            self.BR.setPID(1.0, 0.0, 3.0, 0.0)
            self.scaleToMaxJeffMode()
        self.incrementEncoderTargets()
        #self.ensureSafeDistance()
        self.setWheelsJeffMode()
        self.previousDriveMode = 3
    def invertDrive(self, enabled=True):
        self.invert = -1 if enabled else 1

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
        #self.stores[0] += fixedMagnitude
        self.stores[0] += fixedMagnitude * (math.sin(direction + self.wheelOffset)) * -1 #FL
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

    def incrementEncoderTargets(self):
        if not abs(self.FL.getEncPosition() - self.encoderTargets[0]) > 1000:
            print("incrementing")
            self.encoderTargets[0] += self.stores[0] * self.invert
        if not abs(self.FR.getEncPosition() - self.encoderTargets[1]) > 1000:
            print("incrementing")
            self.encoderTargets[1] += self.stores[1] * self.invert
        if not abs(self.BL.getEncPosition() - self.encoderTargets[2]) > 1000:
            print("incrementing")
            self.encoderTargets[2] += self.stores[2] * self.invert
        if not abs(self.BR.getEncPosition() - self.encoderTargets[3]) > 1000:
            print("incrementing")
            self.encoderTargets[3] += self.stores[3] * self.invert

    def setWheels(self):
        self.FL.set(self.stores[0] * self.invert)
        self.FR.set(self.stores[1] * self.invert)
        self.BL.set(self.stores[2] * self.invert)
        self.BR.set(self.stores[3] * self.invert)
        #print(str(self.stores[0])+ "     "+str(self.stores[1]) + "     "+ str(self.stores[2])+ "     " + str(self.stores[3]))

    def setWheelsJeffMode(self):
        self.FL.set(self.encoderTargets[0])
        self.FR.set(self.encoderTargets[1])
        self.BL.set(self.encoderTargets[2])
        self.BR.set(self.encoderTargets[3])

    def scaleToMax(self):
        for i in range (0,4):
            self.stores[i] *= self.maxVelocity * 5

    def scaleToMaxJeffMode(self):
        for i in range (0,4):
            self.stores[i] *= self.maxVelocity

    def ensureControlMode(self, controlMode):
        if self.FL.getControlMode()\
           == self.FR.getControlMode()\
           == self.BL.getControlMode()\
           == self.BR.getControlMode()\
           == controlMode:
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

    def zeroEncoderTargets(self):
        self.encoderTargets[0] = self.FL.getEncPosition()
        self.encoderTargets[1] = self.FR.getEncPosition()
        self.encoderTargets[2] = self.BL.getEncPosition()
        self.encoderTargets[3] = self.BR.getEncPosition()

    def ensureSafeDistance(self):

        flposition = self.FL.getEncPosition()
        if abs(flposition - self.encoderTargets[0]) > 4000:
            if (self.encoderTargets[0] > flposition):
                self.encoderTargets[0] = flposition + 4000
            else:
                self.encoderTargets[0] = flposition - 4000

        frposition = self.FL.getEncPosition()
        if abs(frposition - self.encoderTargets[0]) > 4000:
            if (self.encoderTargets[0] > frposition):
                self.encoderTargets[0] = frposition + 4000
            else:
                self.encoderTargets[0] = frposition - 4000

        blposition = self.FL.getEncPosition()
        if abs(blposition - self.encoderTargets[0]) > 4000:
            if (self.encoderTargets[0] > blposition):
                self.encoderTargets[0] = blposition + 4000
            else:
                self.encoderTargets[0] = blposition - 4000

        brposition = self.FL.getEncPosition()
        if abs(brposition - self.encoderTargets[0]) > 4000:
            if (self.encoderTargets[0] > brposition):
                self.encoderTargets[0] = brposition + 4000
            else:
                self.encoderTargets[0] = brposition - 4000

    def enableTalons(self):
        self.FL.enable()
        self.FR.enable()
        self.BL.enable()
        self.BR.enable()

    def disableTalons(self):
        self.FL.disable()
        self.FR.disable()
        self.BL.disable()
        self.BR.disable()

    def scaleToMaxJeffModeSlowMode(self):
        for i in range (0,4):
            self.stores[i] *= self.slowModeMaxVelocity

