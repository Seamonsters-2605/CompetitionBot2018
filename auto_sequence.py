import math
import auto_driving
import auto_vision
import auto_shoot
import seamonsters as sea
import auto_navx
import wpilib


def autoSequence(drive, vision):
    switchPosition = wpilib.DriverStation.getInstance().getGameSpecificMessage()
    if len(switchPosition) == 0:
        print("No game message!")
        return
    if switchPosition[0] == "L":
            switchPos1 = 75
            switchPos2 = 120
            switchPos3 = 244
    elif switchPosition[0] == "R":
            switchPos1 = 244
            switchPos2 = 75
            switchPos3 = 75

    else:
        print("Invalid game message!")
        return

    yield from sea.wait(25)
    if wpilib.DriverStation.getInstance().getLocation() == 1:
        if switchPos1 == 75:
            for i in range(50):
                drive.drive(.3, math.pi / 2, 0)
                yield
            drive.drive(0, 0, 0)
            for i in range(switchPos1):
                drive.drive(i/150, 0, 0)
                yield
        elif switchPos1 == 244:
                yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1.6, -1), 225)
                yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1, 0.2), 30)
        drive.drive(0, 0, 0)
    elif wpilib.DriverStation.getInstance().getLocation() == 2:
        if switchPos2 == 75:
            for i in range(50):
                drive.drive(.3, math.pi / 2, 0)
                yield
            drive.drive(0, 0, 0)
            for i in range(switchPos2):
                drive.drive(i/150, 0, 0)
                yield
        elif switchPos2 == 120:
                yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1.6, 1), 100)
                yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1, 0.2), 30)
        drive.drive(0, 0, 0)
    elif wpilib.DriverStation.getInstance().getLocation() == 3:
        if switchPos3 == 244:
            yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1.6, 1), 230)
            yield from sea.timeLimit(auto_driving.driveContinuous(drive, .3, 1, -0.2), 30)
        elif switchPos3 == 75:
            for i in range(50):
                drive.drive(.3, math.pi / 2, 0)
                yield
            drive.drive(0, 0, 0)
            for i in range(switchPos3):
                drive.drive(-i/150, 0, 0)
                yield
        drive.drive(0, 0, 0)
    #yield from sea.wait(25)
    yield from sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0), 20)
    drive.drive(0, 0, 0)
    yield from sea.watch(auto_vision.strafeAlign(drive, vision, 0),
                         drive.drive(.3, math.pi/2, 0), sea.wait(70))
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