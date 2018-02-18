import math
import auto_driving
import auto_vision
import seamonsters as sea
import auto_navx
import wpilib
import auto_strategies

def autoSequence(drive, vision, rotationTracker, shooter):
    switchPosition = wpilib.DriverStation.getInstance().getGameSpecificMessage()
    if not sea.getSwitch("Activate Switch", False):
        if wpilib.DriverStation.getInstance().getLocation() == 1:
            yield from auto_strategies.loc1_crossLine(drive, rotationTracker)
        elif wpilib.DriverStation.getInstance().getLocation() == 2:
            yield from auto_driving.driveDistance(drive, 35, .3)
            yield
            drive.drive(0, 0, 0)
            if switchPosition[0] == "L":
                yield from auto_strategies.loc2_left_crossLine(drive, rotationTracker)
            elif switchPosition[0] == "R":
                yield from auto_strategies.loc2_right_crossLine(drive, rotationTracker)
            for i in range(150):
                drive.drive(.3, math.pi / 2, 0)
                yield
            drive.drive(0, 0, 0)
        elif wpilib.DriverStation.getInstance().getLocation() == 3:
            yield from auto_strategies.loc3_crossLine(drive, rotationTracker)
    else:
        if len(switchPosition) == 0:
            print("No game message!")
            return


        yield from sea.wait(25)
        if wpilib.DriverStation.getInstance().getLocation() == 1:
            if switchPosition[0] == "L":
                yield from auto_strategies.loc1_left_switchFront(drive, rotationTracker)
            if switchPosition[0] == "R":
                yield from auto_strategies.loc1_right_switchFront(drive, rotationTracker)

        elif wpilib.DriverStation.getInstance().getLocation() == 2:
            if switchPosition[0] == "R":
                yield from auto_strategies.loc2_right_switchFront(drive, rotationTracker)
            elif switchPosition[0] == "L":
                yield from auto_strategies.loc2_left_switchFront(drive, rotationTracker)

        elif wpilib.DriverStation.getInstance().getLocation() == 3:
            if switchPosition[0] == "L":
                yield from auto_strategies.loc3_left_switchFront(drive, rotationTracker)
            if switchPosition[0] == "R":
                yield from auto_strategies.loc3_right_switchFront(drive, rotationTracker)


        yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
        yield from sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0),20)
        drive.drive(0, 0, 0)
        yield from sea.watch(auto_driving.driveDistance(drive, 53, .5))
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