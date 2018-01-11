__author__ = "seamonsters"

import math
import wpilib
import ctre
from robotpy_ext.common_drivers.navx import AHRS
import seamonsters as sea

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
        fastPID = (1.0, 0.0009, 3.0, 0.0)
        # speed at which fast PID's should be used:
        fastPIDScale = 0.09
        # PIDF values for slow driving:
        slowPID = (30.0, 0.0009, 3.0, 0.0)
        # speed at which slow PID's should be used:
        slowPIDScale = 0.01

        pidLookBackRange = 10

        maxVelocity = 650

        # encoder has 100 raw ticks -- with a QuadEncoder that makes 400 ticks
        # the motor gear has 12 teeth and the wheel has 85 teeth
        # 85 / 12 * 400 = 2833.333 = ~2833
        ticksPerWheelRotation = 2833

        ### END OF CONSTANTS ###

        self.driverJoystick = wpilib.Joystick(0)

        fl = ctre.CANTalon(2)
        fr = ctre.CANTalon(1)
        bl = ctre.CANTalon(0)
        br = ctre.CANTalon(3)
        self.talons = [fl, fr, bl, br]

        for talon in self.talons:
            talon.setFeedbackDevice(ctre.CANTalon.FeedbackDevice.QuadEncoder)

        self.driveModeLog = sea.LogState("Drive mode")

        self._setPID(fastPID)

        self.holoDrive = sea.HolonomicDrive(fl, fr, bl, br, ticksPerWheelRotation)
        self.holoDrive.invertDrive(True)
        self.holoDrive.setWheelOffset(math.radians(45.0))  # angle of rollers
        self.holoDrive.setMaxVelocity(maxVelocity)

        self.pidDrive = sea.DynamicPIDDrive(self.holoDrive, self.talons,
            slowPID, slowPIDScale, fastPID, fastPIDScale, pidLookBackRange)

        self.ahrs = AHRS.create_spi()  # the NavX
        self.fieldDrive = sea.FieldOrientedDrive(self.pidDrive, self.ahrs,
            offset=0)
        self.fieldDrive.zero()

        self.fieldDriveLog = sea.LogState("Field oriented")

        self.pdp = wpilib.PowerDistributionPanel()
        self.currentLog = sea.LogState("Drive current", logFrequency=2.0)

        self.encoderLog = sea.LogState("Wheel encoders")
        self.speedLog = sea.LogState("Wheel speeds")

    def teleop(self):
        self.holoDrive.zeroEncoderTargets()

        if sea.getSwitch("Field oriented drive", False):
            self.drive = self.fieldDrive
        else:
            self.drive = self.fieldDrive.interface
        if sea.getSwitch("Drive voltage mode", True):
            self.holoDrive.setDriveMode(ctre.CANTalon.ControlMode.PercentVbus)
        else:
            self.holoDrive.setDriveMode(ctre.CANTalon.ControlMode.Position)

        self.encoderLoggingEnabled = sea.getSwitch("Encoder logging", False)

        while True:
            yield
            self.teleopPeriodic()

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
                encoderLogText += str(talon.getPosition()) + " "
            self.encoderLog.update(encoderLogText)
            speedLogText = ""
            for talon in self.talons:
                speedLogText += str(talon.getEncVelocity()) + " "
            self.speedLog.update(speedLogText)

        self.driveModeLog.update(sea.talonModeToString(
            self.holoDrive.driveMode))

        if self.drive is self.fieldDrive:
            self.fieldDriveLog.update("Enabled")
        else:
            self.fieldDriveLog.update("Disabled")

        turn = self.driverJoystick.getTwist()
        magnitude = self.driverJoystick.getMagnitude()
        direction = -self.driverJoystick.getDirectionRadians() + math.pi/2

        magnitude = self._joystickPower(magnitude, self.joystickExponent)\
                    * self.normalScale
        turn = self._joystickPower(turn, self.joystickExponent)\
                    * self.normalTurnScale
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
            talon.setPID(pid[0], pid[1], pid[2], pid[3])

    def _joystickPower(self, value, exponent):
        value = sea.deadZone(value)
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

