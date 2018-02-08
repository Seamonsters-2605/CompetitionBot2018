__author__ = 'seamonsters'

import ctre
import math

import seamonsters.drive


class HolonomicDrive(seamonsters.drive.DriveInterface):
    """
    An implementation of the DriveInterface for holonomic drive. This allows for
    mecanum/omni drives in the "diamond" configuration. The offset of the wheels
    can be changed -- default is .25 pi radians (or 45 degrees), which is ideal
    for our regular mecanum wheels or the typical omni drive's.

    This class can also control a tank drive, although it isn't ideal for that.
    Just set the wheel offset to 0.

    PLEASE READ:

    Right side driving forward is assumed to be +1. Turning counter-clockwise is
    assumed to be +1. Meet these requirements and THEN use invertDrive() if it
    is all backwards. Turn should be passed in as -Joystick.getX, most likely.
    """

    # constants used for wheel indices:
    FRONT_LEFT = 0
    FRONT_RIGHT = 1
    BACK_LEFT = 2
    BACK_RIGHT = 3

    def __init__(self, fl, fr, bl, br):
        self.wheelMotors = [None for i in range(0, 4)]
        self.wheelMotors[HolonomicDrive.FRONT_LEFT] = fl
        self.wheelMotors[HolonomicDrive.FRONT_RIGHT] = fr
        self.wheelMotors[HolonomicDrive.BACK_LEFT] = bl
        self.wheelMotors[HolonomicDrive.BACK_RIGHT] = br

        # stores the currently calculated voltage or velocity that will be sent
        # to the talons, for each wheel
        self.targetVelocities = [0.0, 0.0, 0.0, 0.0]

        # for position mode: stores the current target position for each wheel
        self.targetPositions = [0.0, 0.0, 0.0, 0.0]

        self.wheelOffset = math.pi / 4
        # can be 1 for normal driving, or -1 to invert all motors
        self.invert = 1
        self.maxVelocityPositionMode = 400
        self.maxVelocitySpeedMode = 400 * 5
        self.maxError = 400

        self.driveMode = ctre.ControlMode.PercentOutput
        self.motorState = None

    def invertDrive(self, enabled=True):
        """
        If invertDrive is enabled, all motor directions will be inverted.
        """
        self.invert = -1 if enabled else 1

    def setDriveMode(self, mode):
        self.driveMode = mode

    def drive(self, magnitude, direction, turn):
        mode = self.driveMode
        if mode == ctre.ControlMode.PercentOutput:
            self.driveVoltage(magnitude, direction, turn)
        elif mode == ctre.ControlMode.Velocity:
            self.driveVelocity(magnitude, direction, turn)
        elif mode == ctre.ControlMode.Position:
            self.drivePosition(magnitude, direction, turn)

    def driveVoltage(self, magnitude, direction, turn):
        if turn == 0 and magnitude == 0:
            self._disableMotors()
            return
        self._calcWheels(magnitude, direction, turn)
        self._setMotorVelocities()

    def driveVelocity(self, magnitude, direction, turn):
        if (turn == 0 and magnitude == 0):
            self._disableMotors()
            return
        self._calcWheels(magnitude, direction, turn)
        self._scaleVelocityMode()
        self._setMotorVelocities()

    # Increments positions to mock velocity mode
    def drivePosition(self, magnitude, direction, turn):
        if (turn == 0 and magnitude == 0):
            self._disableMotors()
            return
        if not self._motorsInPositionMode():
            self.resetTargetPositions()
        self._calcWheels(magnitude, direction, turn)
        self._scalePositionMode()
        self._incrementTargetPositions()
        self._setMotorPositions()

    def resetTargetPositions(self):
        for i in range(0, 4):
            self.targetPositions[i] = \
                self.wheelMotors[i].getSelectedSensorPosition(0)

    def _calcWheels(self, magnitude, direction, turn):
        self.targetVelocities = [0.0, 0.0, 0.0, 0.0]
        self._addStrafe(magnitude, direction)
        self._addTurn(turn)
        largest = max([abs(v) for v in self.targetVelocities])
        if largest > 1:
            self.targetVelocities = \
                [number / largest for number in self.targetVelocities]

    def _addStrafe(self, magnitude, direction):
        if magnitude > 1.0:
            magnitude = 1.0
        elif magnitude < -1.0:
            magnitude = -1.0
        self.targetVelocities[HolonomicDrive.FRONT_LEFT] += \
            magnitude * (math.sin(direction + self.wheelOffset)) * -1
        self.targetVelocities[HolonomicDrive.FRONT_RIGHT] += \
            magnitude * (math.sin((direction - self.wheelOffset)))
        self.targetVelocities[HolonomicDrive.BACK_LEFT] += \
            magnitude * (math.sin((direction - self.wheelOffset))) * -1
        self.targetVelocities[HolonomicDrive.BACK_RIGHT] += \
            magnitude * (math.sin((direction + self.wheelOffset)))

    def _addTurn(self, turn):
        for i in range(0, 4):
            self.targetVelocities[i] += turn

    def _incrementTargetPositions(self):
        for i in range(0, 4):
            self.targetPositions[i] += self.targetVelocities[i] * self.invert

    def _scaleVelocityMode(self):
        for i in range(0, 4):
            self.targetVelocities[i] *= self.maxVelocitySpeedMode

    def _scalePositionMode(self):
        for i in range(0, 4):
            self.targetVelocities[i] *= self.maxVelocityPositionMode

    def _setMotorVelocities(self):
        for i in range(0, 4):
            self.wheelMotors[i].set(self.driveMode,
                                    self.targetVelocities[i] * self.invert)
        self.motorState = self.driveMode

    def _setMotorPositions(self):
        for i in range(0, 4):
            currentPos = self.wheelMotors[i].getSelectedSensorPosition(0)
            if abs(currentPos - self.targetPositions[i]) > self.maxError:
                print("Holonomic wheel error!!")
                self.targetPositions[i] = currentPos
            self.wheelMotors[i].set(ctre.ControlMode.Position,
                                    self.targetPositions[i])
        self.motorState = self.driveMode

    def _disableMotors(self):
        if self.motorState == ctre.ControlMode.Disabled:
            return
        for motor in self.wheelMotors:
            motor.disable()
        self.motorState = ctre.ControlMode.Disabled

    def _motorsInPositionMode(self):
        for motor in self.wheelMotors:
            if not motor.getControlMode() == ctre.ControlMode.Position:
                return False
        return True