__author__ = 'Dawson'
import wpilib
import math
from wpilib import CANTalon

from seamonsters.drive import DriveInterface

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

    # constants used for wheel indices:
    FRONT_LEFT = 0
    FRONT_RIGHT = 1
    BACK_LEFT = 2
    BACK_RIGHT = 3

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
        configuration. 1/4 pi is a typical angle for omni/mecanum drives, and is
        the default.
        """
        self.wheelOffset = angleInRadians

    def setMaxVelocity(self, velocity):
        """
        Sets the max encoder velocity. Default is 2000. This number also affects
        the Jeff Mode maximum difference between target and current position,
        although that is also affected by other values.
        """
        self.maxVelocity = velocity
    
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
        self.ensureControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        self.calcWheels(magnitude, direction, turn)
        self.setWheels()
        self.previousDriveMode = DriveInterface.DriveMode.VOLTAGE

    def driveSpeed(self, magnitude, direction, turn):
        self.ensureControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.calcWheels(magnitude, direction, turn)
        self.scaleToMax()
        self.setWheels()
        self.previousDriveMode = DriveInterface.DriveMode.SPEED

    #Increments position to mock speed mode
    def driveSpeedJeffMode(self, magnitude, direction, turn): 
        # if (turn == 0 and magnitude == 0):
        #     self.disableTalons()
        # elif self.FL.getControlMode() == CANTalon.ControlMode.Disabled and\
        #      self.FR.getControlMode() == CANTalon.ControlMode.Disabled and\
        #      self.BL.getControlMode() == CANTalon.ControlMode.Disabled and\
        #      self.BR.getControlMode() == CANTalon.ControlMode.Disabled:
        #     self.enableTalons()
        #     self.zeroEncoderTargets()

        if self.usingInputAccelerationControl:
            filteredResults = \
                    self.accelerationFilter(magnitude, direction, turn)
            magnitude = filteredResults[0]
            direction = filteredResults[1]
            turn = filteredResults[2]

        self.ensureControlMode(wpilib.CANTalon.ControlMode.Position)
        if not self.previousDriveMode == DriveInterface.DriveMode.POSITION:
            self.zeroEncoderTargets()
        self.calcWheels(magnitude, direction, turn)
        self.scaleToMaxJeffMode()
        self.incrementEncoderTargets()
        #self.ensureSafeDistance()
        self.setWheelsJeffMode()
        self.previousDriveMode = DriveInterface.DriveMode.POSITION
    
    
    #DO NOT USE THESE FUNCTIONS

    def calcWheels(self, magnitude, direction, turn):
        self.stores = [0.0, 0.0, 0.0, 0.0]
        self.addStrafe(magnitude, direction)
        self.addTurn(turn)
        self.scaleNumbers()

    def addStrafe(self, magnitude, direction):
        if magnitude > 1.0:
            fixedMagnitude = 1.0
        else:
            fixedMagnitude = magnitude
        self.stores[HolonomicDrive.FRONT_LEFT] += fixedMagnitude \
                * (math.sin(direction + self.wheelOffset)) * -1
        self.stores[HolonomicDrive.FRONT_RIGHT] += fixedMagnitude \
                * (math.sin((direction - self.wheelOffset)))
        self.stores[HolonomicDrive.BACK_LEFT] += fixedMagnitude \
                * (math.sin((direction - self.wheelOffset))) * -1
        self.stores[HolonomicDrive.BACK_RIGHT] += fixedMagnitude \
                * (math.sin((direction + self.wheelOffset)))

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
        if not abs(self.FL.getEncPosition() \
                - self.encoderTargets[HolonomicDrive.FRONT_LEFT]) > 4000:
            self.encoderTargets[HolonomicDrive.FRONT_LEFT] += \
                self.stores[HolonomicDrive.FRONT_LEFT] * self.invert
        
        if not abs(self.FR.getEncPosition() \
                - self.encoderTargets[HolonomicDrive.FRONT_RIGHT]) > 4000:
            self.encoderTargets[HolonomicDrive.FRONT_RIGHT] += \
                self.stores[HolonomicDrive.FRONT_RIGHT] * self.invert
        
        if not abs(self.BL.getEncPosition() \
                - self.encoderTargets[HolonomicDrive.BACK_LEFT]) > 4000:
            self.encoderTargets[HolonomicDrive.BACK_LEFT] += \
                self.stores[HolonomicDrive.BACK_LEFT] * self.invert
        
        if not abs(self.BR.getEncPosition() \
                - self.encoderTargets[3]) > 4000:
            self.encoderTargets[HolonomicDrive.BACK_RIGHT] += \
                self.stores[HolonomicDrive.BACK_RIGHT] * self.invert

    def setWheels(self):
        self.FL.set(self.stores[HolonomicDrive.FRONT_LEFT] * self.invert)
        self.FR.set(self.stores[HolonomicDrive.FRONT_RIGHT] * self.invert)
        self.BL.set(self.stores[HolonomicDrive.BACK_LEFT] * self.invert)
        self.BR.set(self.stores[HolonomicDrive.BACK_RIGHT] * self.invert)

    def setWheelsJeffMode(self):
        self.FL.set(self.encoderTargets[HolonomicDrive.FRONT_LEFT])
        self.FR.set(self.encoderTargets[HolonomicDrive.FRONT_RIGHT])
        self.BL.set(self.encoderTargets[HolonomicDrive.BACK_LEFT])
        self.BR.set(self.encoderTargets[HolonomicDrive.BACK_RIGHT])

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

