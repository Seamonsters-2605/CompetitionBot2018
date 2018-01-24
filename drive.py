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
        self.normalScale = 0.37
        # speed scale when fast button is pressed:
        self.fastScale = 1.0
        # speed scale when slow button is pressed:
        self.slowScale = 0.07
        # normal turning speed scale:
        self.normalTurnScale = 0.25
        # turning speed scale when fast button is pressed
        self.fastTurnScale = 0.34

        self.joystickExponent = 2
        self.fastJoystickExponent = .5
        self.slowJoystickExponent = 4

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

        turn = self.driverJoystick.getTwist()
        magnitude = self.driverJoystick.getMagnitude()
        direction = -self.driverJoystick.getDirectionRadians() + math.pi/2

        magnitude = self._joystickPower(magnitude, self.joystickExponent)\
                    * self.normalScale
        turn = self._joystickPower(turn, self.joystickExponent, 0.1)\
                    * self.normalTurnScale
        if self.automaticDrivePositionMode:
            if magnitude <= self.speedModeThreshold \
                    and abs(turn) <= self.speedModeThreshold:
                self.holoDrive.setDriveMode(ctre.ControlMode.Position)
                self.pidDrive.slowPID = self.slowPID
            else:
                self.holoDrive.setDriveMode(ctre.ControlMode.Velocity)
                self.pidDrive.slowPID = self.slowPIDSpeedMode
        # constrain direction to be between 0 and 2pi
        if direction < 0:
            circles = math.ceil(-direction / (math.pi*2))
            direction += circles * math.pi*2
        direction %= math.pi*2
        direction = self.roundDirection(direction, 0)
        direction = self.roundDirection(direction, math.pi/2.0)
        direction = self.roundDirection(direction, math.pi)
        direction = self.roundDirection(direction, 3.0*math.pi/2.0)
        direction = self.roundDirection(direction, math.pi*2)

        self.drive.drive(magnitude, direction, turn)

    def _setPID(self, pid):
        for talon in self.talons:
            talon.config_kP(0, pid[0], 0)
            talon.config_kI(0, pid[1], 0)
            talon.config_kD(0, pid[2], 0)
            talon.config_kF(0, pid[3], 0)

    def _joystickPower(self, value, exponent, deadZone = 0.08):
        value = sea.deadZone(value, deadZone)
        newValue = float(abs(value)) ** float(exponent)
        if value < 0:
            newValue = -newValue
        return newValue

    def roundDirection(self, value, target):
        if abs(value - target) <= self.driveDirectionDeadZone:
            return target
        else:
            return value


if __name__ == "__main__":
    wpilib.run(DriveBot)

