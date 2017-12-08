__author__ = 'seamonsters'

import ctre
import math

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

    def __init__(self, fl, fr, bl, br, ticksPerWheelRotation):
        """
        Initialize holonomicDrive with for talons. ticksPerWheelRotation MUST
        be for a full wheel rotation, not necessarily a full motor rotation.
        """
        self.wheelMotors = [None for i in range(0, 4)]
        self.wheelMotors[HolonomicDrive.FRONT_LEFT] = fl
        self.wheelMotors[HolonomicDrive.FRONT_RIGHT] = fr
        self.wheelMotors[HolonomicDrive.BACK_LEFT] = bl
        self.wheelMotors[HolonomicDrive.BACK_RIGHT] = br
        
        self.ticksPerWheelRotation = ticksPerWheelRotation

        # stores the currently calculated voltage or velocity that will be sent
        # to the CANTalons, for each wheel
        self.stores = [0.0, 0.0, 0.0, 0.0]
        
        # for position/jeff mode: stores the current target position for each
        # wheel
        self.encoderTargets = [0.0, 0.0, 0.0, 0.0]
        
        self.wheelOffset = math.pi / 4
        
        # can be 1 for normal driving, or -1 to invert all motors
        self.invert = 1
        
        # maximum velocity position/jeff mode; multiplied by 5 for speed mode
        self.maxVelocity = 80 * 5
        
        self.previousDriveMode = DriveInterface.DriveMode.VOLTAGE
        self.driveMode = DriveInterface.DriveMode.VOLTAGE


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
        Sets the max encoder velocity for position/jeff and speed mode.
        Default is 400. For position mode, this is the maximum difference
        between target and current position for every iteration (50 times per
        second). Speed mode behaves similarly, but since wpilib uses units of
        10ths of a second, the velocity value is multiplied by 5.
        """
        self.maxVelocity = velocity

    def setDriveMode(self, mode):
        self.driveMode = mode

    def drive(self, magnitude, direction, turn):
        mode = self.driveMode
        if mode == DriveInterface.DriveMode.VOLTAGE:
            self.driveVoltage(magnitude, direction, turn)
        elif mode == DriveInterface.DriveMode.SPEED:
            self.driveSpeed(magnitude, direction, turn)
        elif mode == DriveInterface.DriveMode.POSITION:
            self.driveSpeedJeffMode(magnitude, direction, turn)
    

    # these functions ignore the current driveMode setting. They are not part of
    # DriveInterface
    
    def driveVoltage(self, magnitude, direction, turn):
        if (turn == 0 and magnitude == 0):
            self._disableTalons()
        elif not self._allTalonsEnabled():
            self._enableTalons()
            self.zeroEncoderTargets()
        
        self._ensureControlMode(ctre.CANTalon.ControlMode.PercentVbus)
        self._calcWheels(magnitude, direction, turn)
        self._setWheels()
        self.previousDriveMode = DriveInterface.DriveMode.VOLTAGE

    def driveSpeed(self, magnitude, direction, turn):
        if (turn == 0 and magnitude == 0):
            self._disableTalons()
        elif not self._allTalonsEnabled():
            self._enableTalons()
            self.zeroEncoderTargets()
        
        self._ensureControlMode(ctre.CANTalon.ControlMode.Speed)
        self._calcWheels(magnitude, direction, turn)
        self._scaleToMax()
        self._setWheels()
        self.previousDriveMode = DriveInterface.DriveMode.SPEED

    #Increments position to mock speed mode
    def driveSpeedJeffMode(self, magnitude, direction, turn): 
        if (turn == 0 and magnitude == 0):
            self._disableTalons()
        elif not self._allTalonsEnabled():
            self._enableTalons()
            self.zeroEncoderTargets()

        self._ensureControlMode(ctre.CANTalon.ControlMode.Position)
        if not self.previousDriveMode == DriveInterface.DriveMode.POSITION:
            self.zeroEncoderTargets()
        self._calcWheels(magnitude, direction, turn)
        self._scaleToMaxJeffMode()
        self._incrementEncoderTargets()
        self._setWheelsJeffMode()
        self.previousDriveMode = DriveInterface.DriveMode.POSITION
        
        
    def logCurrent(self):
        print("FL Current:", str(
            self.wheelMotors[HolonomicDrive.FRONT_LEFT].getOutputCurrent()))
        print("FR Current:", str(
            self.wheelMotors[HolonomicDrive.FRONT_RIGHT].getOutputCurrent()))
        print("BL Current:", str(
            self.wheelMotors[HolonomicDrive.BACK_LEFT].getOutputCurrent()))
        print("BR Current:", str(
            self.wheelMotors[HolonomicDrive.BACK_RIGHT].getOutputCurrent()))

    def zeroEncoderTargets(self):
        for i in range(0, 4):
            self.encoderTargets[i] = self.wheelMotors[i].getPosition()
    
    
    def _calcWheels(self, magnitude, direction, turn):
        self.stores = [0.0, 0.0, 0.0, 0.0]
        self._addStrafe(magnitude, direction)
        self._addTurn(turn)
        self._scaleNumbers()

    def _addStrafe(self, magnitude, direction):
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

    def _addTurn(self, turn):
        for i in range(0,4):
            self.stores[i] += turn

    def _scaleNumbers(self):
        largest = max(self.stores)
        if largest > 1:
            for number in self.stores:
                number = number / largest

    def _incrementEncoderTargets(self):
        for i in range(0, 4):
            if not abs(self.wheelMotors[i].getPosition() \
                    - self.encoderTargets[i]) > self.ticksPerWheelRotation:
                self.encoderTargets[i] += self.stores[i] * self.invert

    def _setWheels(self):
        for i in range(0, 4):
            self.wheelMotors[i].set(self.stores[i] * self.invert)

    def _setWheelsJeffMode(self):
        for i in range(0, 4):
            self.wheelMotors[i].set(self.encoderTargets[i])

    def _scaleToMax(self):
        for i in range(0,4):
            self.stores[i] *= self.maxVelocity * 5

    def _scaleToMaxJeffMode(self):
        for i in range(0,4):
            self.stores[i] *= self.maxVelocity

    def _ensureControlMode(self, controlMode):
        for i in range(0, 4):
            self.wheelMotors[i].changeControlMode(controlMode)
    
    def _enableTalons(self):
        for i in range(0, 4):
            self.wheelMotors[i].enable()

    def _disableTalons(self):
        for i in range(0, 4):
            self.wheelMotors[i].disable()

    def _allTalonsEnabled(self):
        for i in range(0, 4):
            if not self.wheelMotors[i].isControlEnabled():
                return False
        return True