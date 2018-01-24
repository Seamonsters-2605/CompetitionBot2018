__author__ = "seamonsters"

import math
import wpilib
import ctre
from robotpy_ext.common_drivers.navx import AHRS
import seamonsters as sea
import camera

class DriveBot(sea.GeneratorBot):

    def robotInit(self):
        ### CONSTANTS ###

        # normal speed scale, out of 1:
        self.magnitudeScale = 0.45
        # normal turning speed scale:
        self.turnScale = 0.3

        self.magnitudeExponent = 2
        self.twistExponent = 1

        # if the joystick direction is within this number of radians on either
        # side of straight up, left, down, or right, it will be rounded
        self.driveDirectionDeadZone = math.radians(10)

        # PIDF values for fast driving:
        self.fastPID = (1.0, 0.0009, 3.0, 0.0)
        # speed at which fast PID's should be used:
        self.fastPIDScale = 0.09
        # PIDF values for slow driving:
        self.slowPID = (30.0, 0.0009, 3.0, 0.0)
        self.slowPIDSpeedMode = (3.0, 0.0009, 3.0, 0.0)
        # speed at which slow PID's should be used:
        self.slowPIDScale = 0.01

        self.pidLookBackRange = 10

        maxVelocity = 650

        # encoder has 100 raw ticks -- with a QuadEncoder that makes 400 ticks
        # the motor gear has 12 teeth and the wheel has 85 teeth
        # 85 / 12 * 400 = 2833.333 = ~2833
        ticksPerWheelRotation = 2833
        # ticksPerWheelRotation = 83584

        # for switching between speed/position mode
        self.speedModeThreshold = 0.05

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

        self._setPID(self.fastPID)

        self.holoDrive = sea.HolonomicDrive(fl, fr, bl, br,
                                            ticksPerWheelRotation)
        self.holoDrive.invertDrive(True)
        self.holoDrive.setWheelOffset(math.radians(45.0))  # angle of rollers
        self.holoDrive.setMaxVelocity(maxVelocity)

        self.pidDrive = sea.DynamicPIDDrive(self.holoDrive, self.talons,
            self.slowPID, self.slowPIDScale, self.fastPID, self.fastPIDScale,
            self.pidLookBackRange)

        self.ahrs = AHRS.create_spi()  # the NavX
        self.fieldDrive = sea.FieldOrientedDrive(self.pidDrive, self.ahrs,
            offset=0)
        self.fieldDrive.zero()

        self.fieldDriveLog = sea.LogState("Field oriented")

        self.pdp = wpilib.PowerDistributionPanel()
        self.currentLog = sea.LogState("Drive current", logFrequency=2.0)

        self.encoderLog = sea.LogState("Wheel encoders")
        self.speedLog = sea.LogState("Wheel speeds")

        self.driveControlLog = sea.LogState("Drive Control")

        self.driveParamLog = sea.LogState("Drive Params")


    def teleop(self):
        self.holoDrive.resetTargetPositions()

        if sea.getSwitch("Field oriented drive", False):
            self.drive = self.fieldDrive
        else:
            self.drive = self.fieldDrive.interface
        self.automaticDrivePositionMode = \
            sea.getSwitch("Automatic drive position mode", True)
        if sea.getSwitch("Drive speed mode", True) \
                or self.automaticDrivePositionMode:
            self.holoDrive.setDriveMode(ctre.ControlMode.Velocity)
            self.pidDrive.slowPID = self.slowPIDSpeedMode
        elif sea.getSwitch("Drive position mode", False):
            self.holoDrive.setDriveMode(ctre.ControlMode.Position)
            self.pidDrive.slowPID = self.slowPID
        else:
            self.holoDrive.setDriveMode(ctre.ControlMode.PercentOutput)

        self.encoderLoggingEnabled = sea.getSwitch("Encoder logging", False)
        self.testMode = sea.getSwitch("Test Mode", False)

        self.tick = 0
        while True:
            yield
            self.teleopPeriodic()
            sea.sendLogStates()

    def teleopPeriodic(self):
        current = 0
        for talon in self.talons:
            current += talon.getOutputCurrent()
        if current > 50:
            self.currentLog.update(str(current) + "!")
        else:
            self.currentLog.update(current)
        if self.encoderLoggingEnabled:
            encoderLogText = ""
            for talon in self.talons:
                encoderLogText += str(talon.getSelectedSensorPosition(0)) + " "
            self.encoderLog.update(encoderLogText)
            speedLogText = ""
            for talon in self.talons:
                speedLogText += str(talon.getSelectedSensorVelocity(0)) + " "
            self.speedLog.update(speedLogText)

        self.driveModeLog.update(sea.talonModeToString(
            self.talons[0].getControlMode()))

        if self.drive is self.fieldDrive:
            self.fieldDriveLog.update("Enabled")
        else:
            self.fieldDriveLog.update("Disabled")

        # no static switch for control mode
        turn = -self.driverJoystick.getRawAxis(3)
        magnitude = self.driverJoystick.getMagnitude()
        if magnitude == 0:
            direction = 0
        else:
            direction = -self.driverJoystick.getDirectionRadians() + math.pi / 2
            direction = self.roundDirection(direction, math.pi/2)

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

        # FOR TESTING -- TOGGLE TWIST EXPONENTS
        if self.driverJoystick.getRawButtonReleased(2):
            self.magnitudeExponent += 1
            if self.magnitudeExponent == 3:
                self.magnitudeExponent = 1
            print("Magnitude exponent:", self.magnitudeExponent)

        throttle = (self.driverJoystick.getRawAxis(2) - 1.0) / -2.0
        magnitude = self._joystickPower(magnitude, self.magnitudeExponent,
                                        deadzone=0)
        turn = self._joystickPower(turn, self.twistExponent,
                                   deadzone=0)
        turn *= throttle * self.turnScale
        magnitude *= throttle * self.magnitudeScale

        if self.automaticDrivePositionMode:
            if magnitude <= self.speedModeThreshold \
                    and abs(turn) <= self.speedModeThreshold:
                self.holoDrive.setDriveMode(ctre.ControlMode.Position)
                self.pidDrive.slowPID = self.slowPID
            else:
                self.holoDrive.setDriveMode(ctre.ControlMode.Velocity)
                self.pidDrive.slowPID = self.slowPIDSpeedMode

        if self.testMode:
            self.driveParamLog.update(('%.3f' % magnitude) + "," +
                                      str(int(math.degrees(direction))) + "," +
                                      ('%.3f' % turn))
        else:
            self.drive.drive(magnitude, direction, turn)

    def _setPID(self, pid):
        for talon in self.talons:
            talon.config_kP(0, pid[0], 0)
            talon.config_kI(0, pid[1], 0)
            talon.config_kD(0, pid[2], 0)
            talon.config_kF(0, pid[3], 0)

    def _joystickPower(self, value, exponent, deadzone = 0.05):
        if value > deadzone:
            result = (value - deadzone) / (1 - deadzone)
            return result ** float(exponent)
        elif value < -deadzone:
            result = (value + deadzone) / (1 - deadzone)
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

