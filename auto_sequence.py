import math
import auto_driving
import auto_vision
import auto_shoot
import seamonsters as sea
import auto_navx
import wpilib

def right_right(drive):
    for i in range(50):
        drive.drive(.3, math.pi / 2, 0)
        yield
    drive.drive(0, 0, 0)
    for i in range(75):
        drive.drive(-i / 150, 0, 0)
        yield

def right_left(drive):
    yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1.6, 1), 230)
    yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1, -0.2), 30)

def mid_right(drive):
    for i in range(50):
        drive.drive(.3, math.pi / 2, 0)
        yield
    drive.drive(0, 0, 0)
    for i in range(75):
        drive.drive(i / 150, 0, 0)
        yield

def mid_left(drive):
    yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1.6, -1), 225)
    yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1, 0.2), 30)

def left_right(drive):
    yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1.6, -1), 225)
    yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1, 0.2), 30)

def left_left(drive):
    for i in range(50):
        drive.drive(.3, math.pi / 2, 0)
        yield
    for i in range(75):
        drive.drive(i / 150, 0, 0)
        yield

def autoSequence(drive, vision):
    vision.getEntry('camMode').setNumber(0)

    switchPosition = wpilib.DriverStation.getInstance().getGameSpecificMessage()
    startPosition =  wpilib.DriverStation.getInstance().getLocation()
    if len(switchPosition) == 0:
        print("No game message!")
        return

    start_l = {"L": left_left, "R": left_right}
    start_m = {"L": mid_left, "R": mid_right}
    start_r = {"L": right_left, "R": right_right}

    targets = [start_l, start_m, start_r]
    drive_func = targets[startPosition - 1][switchPosition[0]]
    drive_func(drive)
    drive.drive(0, 0, 0)

def autonomous(drive, ahrs, vision):
    multiDrive = sea.MultiDrive(drive)
    yield from sea.parallel(auto_navx.rotation(multiDrive, ahrs),
                            autoSequence(multiDrive, vision), auto_driving.updateMultiDrive(multiDrive))


def findTarget(vision, initialWait, timeLimit):
    """
    Return if the target was found or not
    """
    yield from sea.wait(initialWait)
    ensureFoundTargetGenerator = sea.ensureTrue(
        auto_vision.checkForVisionTarget(vision), 25)
    # foundTarget will be True if ensureFoundTargetGenerator passed
    # and None if the time limit cut it off early
    foundTarget = yield from sea.timeLimit(
        sea.returnValue(ensureFoundTargetGenerator, True),
        timeLimit - initialWait)
    return bool(foundTarget)