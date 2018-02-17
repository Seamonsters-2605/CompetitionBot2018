import math
import auto_driving
import auto_vision
import seamonsters as sea
import auto_navx
import wpilib
import auto_strategies

def autoSequence(drive, vision, rotationTracker):
    switchPosition = wpilib.DriverStation.getInstance().getGameSpecificMessage()
    if not sea.getSwitch("Activate Switch", True):
        if wpilib.DriverStation.getInstance().getLocation() == 1:
            yield from auto_strategies.left_cross(drive, rotationTracker)
        elif wpilib.DriverStation.getInstance().getLocation() == 2:
            yield from auto_driving.driveDistance(drive, 35, .3)
            yield
            drive.drive(0, 0, 0)
            if switchPosition[0] == "L":
                yield from auto_strategies.mid_cross_right(drive, rotationTracker)
            elif switchPosition[0] == "R":
                yield from auto_strategies.mid_cross_left(drive, rotationTracker)
            for i in range(150):
                drive.drive(.3, math.pi / 2, 0)
                yield
            drive.drive(0, 0, 0)
        elif wpilib.DriverStation.getInstance().getLocation() == 3:
            yield from auto_strategies.right_cross(drive, rotationTracker)
    else:
        if len(switchPosition) == 0:
            print("No game message!")
            return


        yield from sea.wait(25)
        if wpilib.DriverStation.getInstance().getLocation() == 1:
            if switchPosition[0] == "L":
                yield from auto_strategies.left_left(drive, rotationTracker)
            if switchPosition[0] == "R":
                yield from auto_strategies.left_right(drive, rotationTracker)

        elif wpilib.DriverStation.getInstance().getLocation() == 2:
            if switchPosition[0] == "R":
                yield from auto_strategies.mid_right(drive, rotationTracker)
            elif switchPosition[0] == "L":
                yield from auto_strategies.mid_left(drive, rotationTracker)

        elif wpilib.DriverStation.getInstance().getLocation() == 3:
            if switchPosition[0] == "L":
                yield from auto_strategies.right_left(drive, rotationTracker)
            if switchPosition[0] == "R":
                yield from auto_strategies.right_right(drive, rotationTracker)

        yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
        yield from sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0),20)
        drive.drive(0, 0, 0)
        yield from sea.watch(
            #auto_vision.strafeAlign(drive, vision, 0),
                             auto_driving.driveDistance(drive, 40, .5))


        drive.drive(0, 0, 0)

def autonomous(drive, ahrs, vision, shooter):
    multiDrive = sea.MultiDrive(drive)
    rotationTracker = auto_navx.RotationTracker(multiDrive, ahrs)
    rotationTracker.resetOrigin()
    rotationTracker.setTargetOffsetRotation(0)
    yield from sea.parallel(
        rotationTracker.rotateToTarget(),autoSequence(multiDrive, vision, rotationTracker),auto_driving.updateMultiDrive(multiDrive))


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