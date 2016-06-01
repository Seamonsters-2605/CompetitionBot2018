__author__ = 'Dawson'
import wpilib
import math
from wpilib import CANTalon

from seamonsters.drive import DriveInterface

BELT_BROKEN = False

class HolonomicDrive(DriveInterface):
    """
    An implementation of the DriveInterface for holonomic drive. This allows for
    mecanum/omni drives in the "diamond" configuration. The offset of the wheels
    can be changed -- default is .25 pi radians (or 45 degrees), which is ideal
    for our regular mecanum wheels or the typical omni drive's. If you want this
    code to work with Jeff's drivetrain just change the angle offset to 27/180
    pi radians (27 degrees).
    
    This class can also control a tank drive, although it isn't ideal for that.
    Just set the wheel offset to 0.
    
    PLEASE READ:
    
    Right side driving forward is assumed to be +1. Turning counter-clockwise is
    assumed to be +1. Meet these requriements and THEN use invertDrive() if it
    is all backwards. Turn should be passed in as -Joystick.getX, most likely.
    """

    def __init__(self, fl, fr, bl, br):
        DriveInterface.__init__(self)
        self.FL = fl
        self.FR = fr
        self.BL = bl
        self.BR = br

        self.stores = [0.0, 0.0, 0.0, 0.0]
        self.encoderTargets = [0.0, 0.0, 0.0, 0.0]
        self.wheelOffset = math.pi / 4
        self.invert = 1 # can be 1 or -1
        # maxVelocity is for "Jeff mode" (aka integral velocity)
        # and is modified for velocity mode
        self.maxVelocity = 80 * 5 
        self.slowModeMaxVelocity = 50
        self.previousDriveMode = DriveInterface.DriveMode.VOLTAGE
        self.driveMode = DriveInterface.DriveMode.VOLTAGE

        self.usingInputAccelerationControl = True
        self.maximumAccelDistance = .08
        self.previousX = 0.0
        self.previousY = 0.0
        self.previousTurn = 0.0
        
    # returns an list of: [magnitude, direction, turn]
    # for internal use only
    def accelerationFilter(self, magnitude, direction, turn):
        newX = magnitude * math.cos(direction)
        newY = magnitude * math.sin(direction)
        distanceToNew = math.sqrt( (newX - self.previousX) ** 2 \
                + (newY - self.previousY) ** 2 )
        finalTurn = turn
        if not abs(self.previousTurn - turn) <= self.maximumAccelDistance:
            if turn > self.previousTurn:
                finalTurn = self.previousTurn + self.maximumAccelDistance
            else:
                finalTurn = self.previousTurn - self.maximumAccelDistance

        if (distanceToNew <= self.maximumAccelDistance):
            self.previousX = newX
            self.previousY = newY
            self.previousTurn = finalTurn
            return [magnitude, direction, finalTurn]

        #Alternate Return for strafe fail to pass
        directionToNew = math.atan2(newY-self.previousY, newX-self.previousX)
        finalX = self.previousX \
                + math.cos(directionToNew) * self.maximumAccelDistance
        finalY = self.previousY \
                + math.sin(directionToNew) * self.maximumAccelDistance
        self.previousX = finalX
        self.previousY = finalY
        self.previousTurn = finalTurn
        return [math.sqrt(finalX ** 2 + finalY ** 2), \
                math.atan2(finalY, finalX), finalTurn]


    #USE THESE FEW FUNCTIONS BELOW
    
    def invertDrive(self, enabled=True):
        """
        If invertDrive is enabled, all motor directions will be inverted.
        """
        self.invert = -1 if enabled else 1

    def setWheelOffset(self, angleInRadians):
        """
        Set the offset angle at which the wheels exert force -- in radians. 0 is
        facing forward (tank drive). 1/4 pi (45 degrees) is a "diamond"
        configuration.
        """
        self.wheelOffset = angleInRadians

    def setMaxVelocity(self, velocity):
        """
        Sets the max encoder velocity. Default is 2000. This number also affects
        the Jeff Mode maximum difference between target and current position.
        """
        self.maxVelocity = velocity
    
    def setDriveMode(self, mode):
        self.driveMode = mode

    def getDriveMode(self):
        return self.driveMode
    
    def drive(self, magnitude, direction, turn, forceDriveMode = None):
        mode = None
        if forceDriveMode == None:
            mode = self.driveMode
        else:
            mode = forceDriveMode
        if mode == DriveInterface.DriveMode.VOLTAGE:
            self.driveVoltage(magnitude, direction, turn)
        elif mode == DriveInterface.DriveMode.SPEED:
            self.driveSpeed(magnitude, direction, turn)
        elif mode == DriveInterface.DriveMode.POSITION:
            self.driveSpeedJeffMode(magnitude, direction, turn)
    

    # these functions ignore the current driveMode setting. They are not part of
    # DriveInterface
    
    def driveVoltage(self, magnitude, direction, turn):
        magnitude *= self.magnitudeScale
        turn *= self.turnScale
        self.ensureControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        self.calcWheels(magnitude, direction, turn)
        self.setWheels()
        self.previousDriveMode = DriveInterface.DriveMode.VOLTAGE
        #self.logCurrent()

    def driveSpeed(self, magnitude, direction, turn):
        magnitude *= self.magnitudeScale
        turn *= self.turnScale
        self.ensureControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.calcWheels(magnitude, direction, turn)
        self.scaleToMax()
        self.setWheels()
        self.previousDriveMode = DriveInterface.DriveMode.SPEED
        #self.logCurrent()

    #Increments position to mock speed mode
    def driveSpeedJeffMode(self, inMagnitude, inDirection, inTurn, \
            inAggressivePID = False): 
        # if (turn == 0 and magnitude == 0):
        #     self.disableTalons()
        # elif self.FL.getControlMode() == CANTalon.ControlMode.Disabled and\
        #      self.FR.getControlMode() == CANTalon.ControlMode.Disabled and\
        #      self.BL.getControlMode() == CANTalon.ControlMode.Disabled and\
        #      self.BR.getControlMode() == CANTalon.ControlMode.Disabled:
        #     self.enableTalons()
        #     self.zeroEncoderTargets()
        
        inMagnitude *= self.magnitudeScale
        inTurn *= self.turnScale
        
        magnitude = inMagnitude
        direction = inDirection
        turn = inTurn
        aggressivePID = inAggressivePID

        if self.usingInputAccelerationControl:
            filteredResults = \
                    self.accelerationFilter(magnitude, direction, turn)
            magnitude = filteredResults[0]
            direction = filteredResults[1]
            turn = filteredResults[2]

        self.ensureControlMode(wpilib.CANTalon.ControlMode.Position)
        if not self.previousDriveMode == 3:
            self.zeroEncoderTargets()
        self.calcWheels(magnitude, direction, turn)
        if aggressivePID:

            self.FL.setPID(12.0, 0.0, 15.0, 0.0)
            self.FR.setPID(12.0, 0.0, 15.0, 0.0)
            self.BL.setPID(12.0, 0.0, 15.0, 0.0)
            self.BR.setPID(12.0, 0.0, 15.0, 0.0)
            self.scaleToMaxJeffMode()
        else:
            self.FL.setPID(1.0, 0.0, 3.0, 0.0)
            self.FR.setPID(1.0, 0.0, 3.0, 0.0)
            self.BL.setPID(1.0, 0.0, 3.0, 0.0)
            self.BR.setPID(1.0, 0.0, 3.0, 0.0)
            self.scaleToMaxJeffMode()
        self.incrementEncoderTargets()
        #self.ensureSafeDistance()
        self.setWheelsJeffMode()
        self.previousDriveMode = DriveInterface.DriveMode.POSITION
    
    
    #DO NOT USE THESE FUNCTIONS

    def calcWheels(self, magnitude, direction, turn):
        self.stores = [0.0, 0.0, 0.0, 0.0]
        self.addStrafe(magnitude, direction)
        if BELT_BROKEN:
            # Now add 1/3 of FR strafe value to entire robots turn,
            # in correct direction
            self.stores[1] *= 2
        if not BELT_BROKEN:
            self.addTurn(turn)
        else:
            self.addTurn(turn - self.stores[1]/8)#1/6 start
        self.scaleNumbers()

    def addStrafe(self, magnitude, direction):
        if magnitude > 1.0:
            fixedMagnitude = 1.0
        else:
            fixedMagnitude = magnitude
        #self.stores[0] += fixedMagnitude
        self.stores[0] += fixedMagnitude \
                * (math.sin(direction + self.wheelOffset)) * -1 #FL
        self.stores[1] += fixedMagnitude \
                * (math.sin((direction - self.wheelOffset))) #FR
        self.stores[2] += fixedMagnitude \
                * (math.sin((direction - self.wheelOffset))) * -1 #BL
        self.stores[3] += fixedMagnitude \
                * (math.sin((direction + self.wheelOffset))) #FR

    def addTurn(self, turn):
        for i in range (0,4):
            self.stores[i] += turn

    def scaleNumbers(self):
        largest = max(self.stores)
        if largest > 1:
            for number in self.stores:
                number = number / largest

    def incrementEncoderTargets(self):
        #Started @ 1000
        if not abs(self.FL.getEncPosition() - self.encoderTargets[0]) > 4000: 
            print(self.FL.getEncPosition())
            self.encoderTargets[0] += self.stores[0] * self.invert
        if not abs(self.FR.getEncPosition() - self.encoderTargets[1]) > 4000:
            #print("incrementing")
            self.encoderTargets[1] += self.stores[1] * self.invert
        if not abs(self.BL.getEncPosition() - self.encoderTargets[2]) > 4000:
            #print("incrementing")
            self.encoderTargets[2] += self.stores[2] * self.invert
        if not abs(self.BR.getEncPosition() - self.encoderTargets[3]) > 4000:
            #print("incrementing")
            self.encoderTargets[3] += self.stores[3] * self.invert

    def setWheels(self):
        self.FL.set(self.stores[0] * self.invert)
        self.FR.set(self.stores[1] * self.invert)
        self.BL.set(self.stores[2] * self.invert)
        self.BR.set(self.stores[3] * self.invert)

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
        # TODO: add counts per rev. variable, and max velocity variable
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

