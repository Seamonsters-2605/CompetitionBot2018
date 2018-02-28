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
        self.turnScales = (0.15, 0.20, 0.35)

        # Tad's vars

        self.turnRampUp = 1.3 # this is a multiplier
        self.magnitudeRampUp = 1.3 # this is a multiplier

        self.rampUpDelay = .5
        self.rampUpTime = 1.5

        ### END OF CONSTANTS ###

        try:
            self.driverJoystick
        except AttributeError:
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

        self.directionLog = sea.LogState("Direction")

        self.driveParamLog = sea.LogState("Drive Params")

        self.vision = NetworkTables.getTable('limelight')

        self.currentPIDs = None


    def teleop(self):
        #for talon in self.talons:
        #    talon.setSelectedSensorPosition(0, 0, 10)

        self.reversed = True # start going towards intake
        self.vision.getEntry('ledMode').setNumber(1) # off
        self.vision.getEntry('camMode').setNumber(1) # driver camera

        self.holoDrive.resetTargetPositions()

        self.tick = 0
        try:
            while True:
                yield
                self.teleopPeriodic()
        finally:
            self.drive.drive(0, 0, 0)

    def autonomous(self):
        print("Starting autonomous!")
        #for talon in self.talons:
        #    talon.setSelectedSensorPosition(0, 0, 10)

        sea.setActiveCameraURL('')
        self.vision.getEntry('ledMode').setNumber(0) # on
        self.vision.getEntry('camMode').setNumber(0) # vision processing

        self.holoDrive.resetTargetPositions()
        self.holoDrive.setDriveMode(ctre.ControlMode.Velocity)
        self._setPID(robotconfig.positionModePIDs[0])
        yield from auto_sequence.autonomous(
            self.holoDrive, self.ahrs, self.vision, self.theRobot.shooterBot)
        print("Auto sequence complete!")

    def teleopPeriodic(self):
        if sea.getSwitch("Current logging", False):
            current = 0
            for talon in self.talons:
                current += talon.getOutputCurrent()
                pass
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

        self.driveModeLog.update(self.holoDrive.motorState)

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
        strafe = self.driverJoystick.getRawAxis(4)
        turn = -self.driverJoystick.getX() - self.driverJoystick.getRawAxis(3)

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
        """if self.driverJoystick.getRawButtonReleased(2):
            self.magnitudeExponent += 1
            if self.magnitudeExponent == 3:
                self.magnitudeExponent = 1
            print("Magnitude exponent:", self.magnitudeExponent)"""

        fwd = self._joystickPower(fwd, self.magnitudeExponent, deadzone=0)
        strafe = self._joystickPower(strafe, self.magnitudeExponent, deadzone=0)
        turn = self._joystickPower(turn, self.twistExponent, deadzone=0)
        fwd *= self.forwardScales[gear]
        strafe *= self.strafeScales[gear]
        turn *= self.turnScales[gear]

        magnitude = math.sqrt(fwd**2 + strafe**2)
        direction = -math.atan2(fwd, strafe)
        direction = self.roundDirection(direction, math.pi/2)

        pov = self.driverJoystick.getPOV()
        if pov == 90:
            gear = 0
            magnitude = .20
            direction = 0
            turn = .08
        if pov == 270:
            gear = 0
            magnitude = .20
            direction = math.pi
            turn = -.08

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
        if self.driverJoystick.getRawButton(1):
            self._setPID(robotconfig.speedModePIDs[2])
            for talon in self.talons:
                talon.set(ctre.ControlMode.Velocity, 0)
        elif not sea.getSwitch("DON'T DRIVE", False):
            if self.reversed:
                self.directionLog.update("Towards intake")
                sea.setActiveCameraURL('http://10.26.5.2:1187/stream.mjpg')
                self.drive.drive(magnitude, direction + math.pi, turn)
            else:
                self.directionLog.update("Towards shooter")
                sea.setActiveCameraURL('http://10.26.5.6:5800')
                self.drive.drive(magnitude, direction, turn)

        if self.driverJoystick.getRawButtonPressed(4):
            self.reversed = not self.reversed


    def test(self):
        for talon in self.talons:
            talon.setSelectedSensorPosition(0, 0, 10)

        self.holoDrive.resetTargetPositions()

        targetRealArea = 122.4
        dist = 120
        focal8 = 11.538400625742273
        focal10 = 11.056585532507528

        avgAreas = [0]*5

        borkCount = 0

        for n in range(5):
            areaSum = 0
            sumTicks = 200
            for i in range(sumTicks):
                yield
                area = self.vision.getNumber('ta', "It borked")
                try:
                    areaSum += area
                except:
                    sumTicks -= 1

                self.drive = self.fieldDrive
                self.drive.drive(0, 0, 0)
            avgAreas[n] = areaSum / sumTicks
            print("Avg area " + str(n) + ": " + str(areaSum / sumTicks))

        overallAvg = 0
        for i in avgAreas:
            overallAvg += i
        overallAvg *= 1/5

        estFocal = dist * math.sqrt(overallAvg) / math.sqrt(targetRealArea)

        print("Est. Focal Dist: " + str(estFocal))

        estDist = focal8 * math.sqrt(targetRealArea) / math.sqrt(overallAvg)
        print("Est. Dist: " + str(estDist))

    def _setPID(self, pid):
        if pid == self.currentPIDs:
            return
        for talon in self.talons:
            talon.config_kP(0, pid[0], 0)
            talon.config_kI(0, pid[1], 0)
            talon.config_kD(0, pid[2], 0)
            talon.config_kF(0, pid[3], 0)
        self.currentPIDs = pid

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

