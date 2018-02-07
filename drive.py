__author__ = "seamonsters"

import math
import wpilib
import ctre
from robotpy_ext.common_drivers.navx import AHRS
from networktables import NetworkTables
import seamonsters as sea
import camera
import robotconfig
import auto_sequence
import rotation_align


class DriveBot(sea.GeneratorBot):

    def robotInit(self):
        ### CONSTANTS ###
        self.magnitudeExponent = 2
        self.twistExponent = 1

        # if the joystick direction is within this number of radians on either
        # side of straight up, left, down, or right, it will be rounded
        self.driveDirectionDeadZone = math.radians(10)

        self.pidLookBackRange = 10

        self.strafeScales = (0.1, 0.2, 0.2)
        self.forwardScales = (0.15, 0.5, 1.0)
        self.turnScales = (0.05, 0.20, 0.35)

        # Tad's vars

        self.turnRampUp = 1.3 # this is a multiplier
        self.magnitudeRampUp = 1.3 # this is a multiplier

        self.rampUpDelay = .5
        self.rampUpTime = 1.5

        ### END OF CONSTANTS ###

        self.driverJoystick = wpilib.Joystick(0)

        fl = ctre.WPI_TalonSRX(2)
        fr = ctre.WPI_TalonSRX(1)
        bl = ctre.WPI_TalonSRX(0)
        br = ctre.WPI_TalonSRX(3)
        self.talons = [fl, fr, bl, br]

        for talon in self.talons:
            talon.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, 0)

        self.driveModeLog = sea.LogState("Drive mode")

        self.holoDrive = sea.HolonomicDrive(fl, fr, bl, br)
        self.holoDrive.invertDrive(True)
        self.holoDrive.maxError = robotconfig.maxError
        self.holoDrive.maxVelocityPositionMode = robotconfig.maxVelocityPositionMode
        self.holoDrive.maxVelocitySpeedMode = robotconfig.maxVelocitySpeedMode

        self.ahrs = AHRS.create_spi()  # the NavX
        self.fieldDrive = sea.FieldOrientedDrive(self.holoDrive, self.ahrs,
            offset=0)
        self.fieldDrive.zero()

        self.fieldDriveLog = sea.LogState("Field oriented")

        self.pdp = wpilib.PowerDistributionPanel()
        self.currentLog = sea.LogState("Drive current", logFrequency=2.0)

        self.encoderLog = sea.LogState("Wheel encoders")
        self.speedLog = sea.LogState("Wheel speeds")

        self.driveControlLog = sea.LogState("Drive Control")

        self.driveParamLog = sea.LogState("Drive Params")

        self.vision = NetworkTables.getTable('limelight')


    def teleop(self):
        for talon in self.talons:
            talon.setSelectedSensorPosition(0, 0, 10)

        self.holoDrive.resetTargetPositions()

        self.tick = 0
        while True:
            yield
            self.teleopPeriodic()
            sea.sendLogStates()

    def autonomous(self):
        print("Starting autonomous!")
        for talon in self.talons:
            talon.setSelectedSensorPosition(0, 0, 10)

        self.holoDrive.resetTargetPositions()
        self.holoDrive.setDriveMode(ctre.ControlMode.Position)
        self._setPID(robotconfig.positionModePIDs[1])
        yield from sea.parallel(self.sendLogStatesGenerator(),
            auto_sequence.autonomous(self.holoDrive, self.ahrs, self.vision))
        print("Auto sequence complete!")

    def sendLogStatesGenerator(self):
        while True:
            yield
            sea.sendLogStates()

    def teleopPeriodic(self):
        current = 0
        for talon in self.talons:
            current += talon.getOutputCurrent()
        if current > 50:
            self.currentLog.update(str(current) + "!")
        else:
            self.currentLog.update(current)
        if sea.getSwitch("Encoder logging", False):
            encoderLogText = ""
            for talon in self.talons:
                encoderLogText += str(talon.getSelectedSensorPosition(0)) + " "
            self.encoderLog.update(encoderLogText)
            speedLogText = ""
            for talon in self.talons:
                speedLogText += str(talon.getSelectedSensorVelocity(0)) + " "
            self.speedLog.update(speedLogText)

        if sea.getSwitch("Field oriented drive", False):
            self.drive = self.fieldDrive
        else:
            self.drive = self.fieldDrive.interface

        self.driveModeLog.update(sea.talonModeToString(
            self.talons[0].getControlMode()))

        if self.drive is self.fieldDrive:
            robotOffset = self.fieldDrive.getRobotOffset()
            self.fieldDriveLog.update(int(math.degrees(robotOffset)))
        else:
            self.fieldDriveLog.update("Disabled")

        if self.driverJoystick.getRawButton(4):
            self.fieldDrive.zero()

        # 3 possible positions of the throttle
        gear = 2 - round(self.driverJoystick.getRawAxis(2) + 1.0)

        fwd = self.driverJoystick.getY()
        strafe = self.driverJoystick.getX()
        turn = -self.driverJoystick.getRawAxis(3) \
               - self.driverJoystick.getRawAxis(4)

        # Ramp up
        """if turn == 1:
            print("RAMPING UP")
            self.tick += 1

            delayTicks = self.rampUpDelay * 50
            timeTicks = self.rampUpTime * 50

            if self.tick > delayTicks:
                mult = (self.tick - delayTicks) / timeTicks
                if mult > 1:
                    mult = 1
                mult *= (self.turnRampUp - 1)

                turn *= (1 + mult)
        else:
            self.tick = 0"""

        # FOR TESTING -- TOGGLE JOYSTICK EXPONENTS
        if self.driverJoystick.getRawButtonReleased(2):
            self.magnitudeExponent += 1
            if self.magnitudeExponent == 3:
                self.magnitudeExponent = 1
            print("Magnitude exponent:", self.magnitudeExponent)

        fwd = self._joystickPower(fwd, self.magnitudeExponent, deadzone=0)
        strafe = self._joystickPower(strafe, self.magnitudeExponent, deadzone=0)
        turn = self._joystickPower(turn, self.twistExponent, deadzone=0)
        fwd *= self.forwardScales[gear]
        strafe *= self.strafeScales[gear]
        turn *= self.turnScales[gear]

        magnitude = math.sqrt(fwd**2 + strafe**2)
        direction = -math.atan2(fwd, strafe)
        direction = self.roundDirection(direction, math.pi/2)

        if sea.getSwitch("Drive voltage mode", False):
            self.holoDrive.setDriveMode(ctre.ControlMode.PercentOutput)
        elif gear != 0:
            self.holoDrive.setDriveMode(ctre.ControlMode.Velocity)
            self._setPID(robotconfig.speedModePIDs[gear])
        else:
            self.holoDrive.setDriveMode(ctre.ControlMode.Position)
            self._setPID(robotconfig.positionModePIDs[gear])


        if sea.getSwitch("Drive param logging", False):
            self.driveParamLog.update(('%.3f' % magnitude) + "," +
                                      str(int(math.degrees(direction))) + "," +
                                      ('%.3f' % turn))
        elif self.driverJoystick.getRawButton(1):
            self._setPID(robotconfig.speedModePIDs[2])
            for talon in self.talons:
                talon.set(ctre.ControlMode.Velocity, 0)
        elif not sea.getSwitch("DON'T DRIVE", False):
            self.drive.drive(magnitude, direction, turn)

    def test(self):
        for talon in self.talons:
            talon.setSelectedSensorPosition(0, 0, 10)

        self.holoDrive.resetTargetPositions()

        while True:
            yield
            area = self.vision.getNumber('ta', "It borked")
            print("Area: " + str(area))

    def _setPID(self, pid):
        for talon in self.talons:
            talon.config_kP(0, pid[0], 0)
            talon.config_kI(0, pid[1], 0)
            talon.config_kD(0, pid[2], 0)
            talon.config_kF(0, pid[3], 0)

    def _joystickPower(self, value, exponent, deadzone = 0.05):
        if value > deadzone:
            result = (value - deadzone) / (1 - deadzone)
            if result > 1:
                return 1.0
            return result ** float(exponent)
        elif value < -deadzone:
            result = (value + deadzone) / (1 - deadzone)
            if result < -1:
                return -1.0
            return -(abs(result) ** float(exponent))
        else:
            return 0

    def roundDirection(self, value, increment):
        roundedValue = round(float(value) / increment) * increment
        if abs(roundedValue - value) < self.driveDirectionDeadZone:
            return roundedValue
        return value


if __name__ == "__main__":
    wpilib.run(DriveBot)

