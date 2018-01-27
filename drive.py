__author__ = "seamonsters"

import math
import wpilib
import ctre
from robotpy_ext.common_drivers.navx import AHRS
import seamonsters as sea
import camera
import robotconfig

class DriveBot(sea.GeneratorBot):

    def robotInit(self):
        ### CONSTANTS ###
        self.magnitudeExponent = 2
        self.twistExponent = 1

        # if the joystick direction is within this number of radians on either
        # side of straight up, left, down, or right, it will be rounded
        self.driveDirectionDeadZone = math.radians(10)

        self.pidLookBackRange = 10

        # for switching between speed/position mode
        self.speedModeThreshold = 0.05

        # Tad's vars

        self.turnRampUp = 1.3 # this is a multiplier
        self.magnitudeRampUp = 1.3 # this is a multiplier

        self.rampUpDelay = .5
        self.rampUpTime = 1.5

        self.magnitudeCapped = True

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

        self._setPID(robotconfig.fastPID)

        self.holoDrive = sea.HolonomicDrive(fl, fr, bl, br)
        self.holoDrive.invertDrive(True)
        self.holoDrive.maxError = robotconfig.maxError
        self.holoDrive.maxVelocityPositionMode = robotconfig.maxVelocityPositionMode
        self.holoDrive.maxVelocitySpeedMode = robotconfig.maxVelocitySpeedMode

        self.pidDrive = sea.DynamicPIDDrive(self.holoDrive, self.talons,
                                            robotconfig.slowPID, robotconfig.slowPIDScale,
                                            robotconfig.fastPID, robotconfig.fastPIDScale,
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
        for talon in self.talons:
            talon.setSelectedSensorPosition(0, 0, 10)

        self.holoDrive.resetTargetPositions()

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

        # FOR TESTING -- TOGGLE JOYSTICK EXPONENTS
        if self.driverJoystick.getRawButtonReleased(2):
            self.magnitudeExponent += 1
            if self.magnitudeExponent == 3:
                self.magnitudeExponent = 1
            print("Magnitude exponent:", self.magnitudeExponent)

        # FOR TESTING -- TOGGLE MAGNITUDE CAP
        if self.driverJoystick.getRawButtonReleased(3):
            self.magnitudeCapped = not self.magnitudeCapped

        if self.magnitudeCapped and magnitude > 1:
            magnitude = 1

        throttle = (self.driverJoystick.getRawAxis(2) - 1.0) / -2.0
        magnitude = self._joystickPower(magnitude, self.magnitudeExponent,
                                        deadzone=0)
        turn = self._joystickPower(turn, self.twistExponent,
                                   deadzone=0)
        turn *= throttle * robotconfig.turnScale
        magnitude *= throttle * robotconfig.magnitudeScale

        mode = ctre.ControlMode.PercentOutput
        if sea.getSwitch("Drive speed mode", False):
            mode = ctre.ControlMode.Velocity
        elif sea.getSwitch("Drive position mode", False):
            mode = ctre.ControlMode.Position
        if sea.getSwitch("Automatic drive position mode",
                         robotconfig.theRobot=="Leviathan"):
            if magnitude <= self.speedModeThreshold \
                    and abs(turn) <= self.speedModeThreshold:
                mode = ctre.ControlMode.Position
            else:
                mode = ctre.ControlMode.Velocity
        self.holoDrive.setDriveMode(mode)
        if mode == ctre.ControlMode.Position:
            self.pidDrive.slowPID = robotconfig.slowPID
            self.pidDrive.fastPID = robotconfig.fastPID
        elif mode == ctre.ControlMode.Velocity:
            self.pidDrive.slowPID = robotconfig.slowPIDSpeedMode
            self.pidDrive.fastPID = robotconfig.fastPIDSpeedMode

        if sea.getSwitch("Drive param logging", False):
            self.driveParamLog.update(('%.3f' % magnitude) + "," +
                                      str(int(math.degrees(direction))) + "," +
                                      ('%.3f' % turn))
        if not sea.getSwitch("DON'T DRIVE", False):
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

