__author__ = "seamonsters"

import ctre
import math


def talonModeToString(mode):
    """
    Get a readable name from a ``ctre.ControlMode`` constant
    :param mode: a constant from ``ctre.ControlMode``
    :return: a string name
    """
    if mode == ctre.ControlMode.Disabled:
        return "Disabled"
    elif mode == ctre.ControlMode.PercentOutput:
        return "PercentOutput"
    elif mode == ctre.ControlMode.Position:
        return "Position"
    elif mode == ctre.ControlMode.Velocity:
        return "Velocity"
    elif mode == ctre.ControlMode.Current:
        return "Current"
    elif mode == ctre.ControlMode.Follower:
        return "Follower"
    elif mode == ctre.ControlMode.MotionProfile:
        return "MotionProfile"
    else:
        return str(mode)


class DriveInterface:
    """
    A generic, abstract interface for driving a robot.
    """

    def drive(self, magnitude, direction, turn):
        """
        Drive the robot, with a given magnitude, direction, and turn.

        Magnitude: 0 to 1

        Direction: Counterclockwise positive, radians

        Turn: -1 to 1
        """
        pass


class TestDriveInterface(DriveInterface):
    """
    A DriveInterface which does nothing but log the magnitude/direction/turn
    values it receives.
    """

    def drive(self, magnitude, direction, turn):
        print("Drive mag", magnitude, "dir", direction, "turn", turn)


class AccelerationFilterDrive(DriveInterface):
    """
    Wraps another drive interface, and provides acceleration filtering.
    """

    def __init__(self, interface, accelerationRate=.08):
        """
        ``interface`` is the DriveInterface to provide acceleration filtering
        for. ``accelerationRate`` defaults to .08 (0 to full speed in .25
        seconds).
        """
        self.interface = interface

        self.accelerationRate = accelerationRate
        self.previousX = 0.0
        self.previousY = 0.0
        self.previousTurn = 0.0

    def drive(self, magnitude, direction, turn):
        magnitude, direction, turn = \
            self._accelerationFilter(magnitude, direction, turn)
        self.interface.drive(magnitude, direction, turn)

    def getFilteredMagnitude(self):
        return math.sqrt(self.previousX ** 2 + self.previousY ** 2)

    def getFilteredDirection(self):
        return math.atan2(self.previousY, self.previousX)

    def getFilteredTurn(self):
        return self.previousTurn

    # returns an tuple of: (magnitude, direction, turn)
    def _accelerationFilter(self, magnitude, direction, turn):
        if abs(self.previousTurn - turn) <= self.accelerationRate:
            newTurn = turn
        else:
            if turn > self.previousTurn:
                newTurn = self.previousTurn + self.accelerationRate
            else:
                newTurn = self.previousTurn - self.accelerationRate

        x = magnitude * math.cos(direction)
        y = magnitude * math.sin(direction)
        distanceToNew = math.sqrt((x - self.previousX) ** 2 \
                                  + (y - self.previousY) ** 2)

        if distanceToNew <= self.accelerationRate:
            newX = x
            newY = y
            newMagnitude = magnitude
            newDirection = direction
        else:
            directionToNew = math.atan2(y - self.previousY, x - self.previousX)
            newX = self.previousX \
                   + math.cos(directionToNew) * self.accelerationRate
            newY = self.previousY \
                   + math.sin(directionToNew) * self.accelerationRate
            newMagnitude = math.sqrt(newX ** 2 + newY ** 2)
            newDirection = math.atan2(newY, newX)

        self.previousX = newX
        self.previousY = newY
        self.previousTurn = newTurn
        return newMagnitude, newDirection, newTurn


class FieldOrientedDrive(DriveInterface):
    """
    Wraps another drive interface, and provides field orientation.
    """

    def __init__(self, interface, ahrs, offset=0.0):
        """
        Create the FieldOrientedDrive with another DriveInterface to wrap and a
        ``robotpy_ext.common_drivers.navx.AHRS``. If given, the offset is a
        value in radians to add to all direction inputs.
        """
        self.interface = interface
        self.ahrs = ahrs
        self.origin = 0.0
        self.offset = offset

    def zero(self):
        self.origin = self._getYawRadians()

    def drive(self, magnitude, direction, turn):
        direction -= self.getRobotOffset()
        self.interface.drive(magnitude, direction, turn)

    def _getYawRadians(self):
        return - math.radians(self.ahrs.getAngle())

    def getRobotOffset(self):
        return self._getYawRadians() - self.origin - self.offset


class DynamicPIDDrive(DriveInterface):
    """
    Wraps another drive interface. Based on the driving matnitude and turn
    speed, the PID's of a set of talons are changed. PID's are given as a tuple
    of (p, i, d, f). For speeds below ``slowPIDScale``, ``slowPID`` is used.
    For speeds above ``fastPIDScale``, ``fastPID`` is used. For speeds in
    between, the P/I/D/F values are interpolated.
    """

    def __init__(self, interface, wheelTalons, slowPID, slowPIDScale,
                 fastPID, fastPIDScale, pidLookBackRange=10):
        super().__init__()
        self.interface = interface
        self.talons = wheelTalons
        self.slowPID = slowPID
        self.slowPIDScale = slowPIDScale
        self.fastPID = fastPID
        self.fastPIDScale = fastPIDScale

        self.currentPID = None
        self.driveScales = [0.0 for i in range(0, pidLookBackRange)]

    def drive(self, magnitude, direction, turn):
        driveScale = max(abs(magnitude), abs(turn * 2))
        self.driveScales.append(driveScale)
        self.driveScales.pop(0)
        self._setPID(self._lerpPID(max(self.driveScales)))

        self.interface.drive(magnitude, direction, turn)

    def _setPID(self, pid):
        if pid == self.currentPID:
            return
        self.currentPID = pid
        for talon in self.talons:
            talon.config_kP(0, pid[0], 0)
            talon.config_kI(0, pid[1], 0)
            talon.config_kD(0, pid[2], 0)
            talon.config_kF(0, pid[3], 0)

    def _lerpPID(self, magnitude):
        if magnitude <= self.slowPIDScale:
            return self.slowPID
        elif magnitude >= self.fastPIDScale:
            return self.fastPID
        else:
            # 0 - 1
            scale = (magnitude - self.slowPIDScale) / \
                    (self.fastPIDScale - self.slowPIDScale)
            pidList = []
            for i in range(0, 4):
                slowValue = self.slowPID[i]
                fastValue = self.fastPID[i]
                value = (fastValue - slowValue) * scale + slowValue
                pidList.append(value)
            return tuple(pidList)


class MultiDrive(DriveInterface):
    """
    Wraps another DriveInterface, and allows ``drive()`` to be called multiple
    times in a loop. The values for all of these calls are averaged together,
    and sent to the wrapped interface when ``update()`` is called.
    """

    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self._reset()

    def _reset(self):
        self.totalX = 0
        self.totalY = 0
        self.totalTurn = 0
        self.numDriveCalls = 0
        self.numTurnCalls = 0

    def drive(self, magnitude, direction, turn):
        self.totalX += magnitude * math.cos(direction)
        self.totalY += magnitude * math.sin(direction)
        self.totalTurn += turn

        if magnitude != 0:
            self.numDriveCalls += 1
        if turn != 0:
            self.numTurnCalls += 1

    def update(self):
        if self.numDriveCalls == 0:
            x = 0
            y = 0
        else:
            x = float(self.totalX) / float(self.numDriveCalls)
            y = float(self.totalY) / float(self.numDriveCalls)
        if self.numTurnCalls == 0:
            turn = 0
        else:
            turn = float(self.totalTurn) / float(self.numTurnCalls)
        magnitude = math.sqrt(x ** 2 + y ** 2)
        direction = math.atan2(y, x)
        self.interface.drive(magnitude, direction, turn)
        self._reset()


if __name__ == "__main__":
    # test acceleration filter drive
    filterDrive = AccelerationFilterDrive(TestDriveInterface())
    for i in range(0, 20):
        filterDrive.drive(1.0, 1.0, 1.0)
