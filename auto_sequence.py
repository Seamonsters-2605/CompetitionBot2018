import math
import auto_driving
import auto_vision
import seamonsters as sea
import auto_navx
import wpilib
import auto_strategies

def autoSequence(drive, vision, rotationTracker, shooter):
    location = wpilib.DriverStation.getInstance().getLocation()
    gameMessage = wpilib.DriverStation.getInstance().getGameSpecificMessage()
    if gameMessage is None or gameMessage == "":
        yield
        return
    switchPosition = gameMessage[0]
    strategy = auto_strategies.STRAT_SWITCHFRONT \
        if sea.getSwitch("Activate Switch", True) \
        else auto_strategies.STRAT_CROSSLINE

    print("Location:", location)
    print("Switch position:", switchPosition)
    print("Strategy:", strategy)

    stratGenerator = auto_strategies.LOCATION_STRATEGIES[location]\
        [switchPosition][strategy]
    yield from stratGenerator(drive, rotationTracker)

    if strategy == auto_strategies.STRAT_SWITCHFRONT:
        yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
        yield from sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0), 20)
        drive.drive(0, 0, 0)
        yield from sea.watch(auto_driving.driveDistance(drive, 53, .5))
        drive.drive(0, 0, 0)
        yield from shooter.shootGenerator()

    if strategy == auto_strategies.STRAT_SWITCHSIDE:
        yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
        yield from auto_driving.driveDistance(drive, 25, .5)
        drive.drive(0, 0, 0)
        yield from shooter.shootGenerator()

def autonomous(drive, ahrs, vision, shooter):
    multiDrive = sea.MultiDrive(drive)
    rotationTracker = auto_navx.RotationTracker(multiDrive, ahrs)
    rotationTracker.resetOrigin()
    rotationTracker.setTargetOffsetRotation(0)
    yield from sea.parallel(
        rotationTracker.rotateToTarget(),autoSequence(multiDrive, vision, rotationTracker, shooter),auto_driving.updateMultiDrive(multiDrive))


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