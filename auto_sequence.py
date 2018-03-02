import math
import auto_driving
import auto_vision
import seamonsters as sea
import auto_navx
import wpilib
import auto_strategies
import auto_override

def autoSequence(drive, vision, rotationTracker, shooter):
    shooter.stop() # it sometimes is running when auto starts?

    gameMessage = wpilib.DriverStation.getInstance().getGameSpecificMessage()
    if gameMessage is None or gameMessage == "":
        switchPosition = "ERROR!" # will cause it to default to CROSSLINE
    else:
        switchPosition = gameMessage[0]

    startPos = auto_override.override()
    strategy = None
    for strat in auto_strategies.STRATEGIES:
        switchName = switchPosition + " " + strat
        if sea.getSwitch(switchName, False):
            strategy = strat
    if strategy is None:
        strategy = auto_strategies.STRAT_CROSSLINE

    print("Location:", startPos)
    print("Switch position:", switchPosition)
    print("Strategy:", strategy)
    if switchPosition == "ERROR!":
        switchPosition = 'L'

    try:
        stratGenerator = auto_strategies.LOCATION_STRATEGIES[startPos]\
            [switchPosition][strategy]
    except KeyError:
        print("You chose an invalid auto sequence! Defaulting to Cross line")
        strategy = auto_strategies.STRAT_CROSSLINE
        stratGenerator = auto_strategies.LOCATION_STRATEGIES[startPos]\
            [switchPosition][strategy]

    yield from stratGenerator(drive, rotationTracker)

    if strategy == auto_strategies.STRAT_SWITCHFRONT:
        yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
        if (yield from auto_vision.waitForVision(vision)):
            yield from sea.timeLimit(sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0),
                                      20), 100)
        else:
            print("Couldn't find vision!")
        drive.drive(0, 0, 0)
        yield from sea.timeLimit(auto_driving.driveDistance(drive, 53, .5), 50)
        drive.drive(0, 0, 0)
        yield from shootFinal(drive, shooter, rotationTracker)

    if strategy == auto_strategies.STRAT_SWITCHSIDE:
        yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
        yield from sea.timeLimit(auto_driving.driveDistance(drive, 30, .5), 50)
        drive.drive(0, 0, 0)
        yield from shootFinal(drive, shooter, rotationTracker)

    if strategy == auto_strategies.STRAT_EXCHANGE:
        yield from auto_driving.driveDistance(drive, -10, -.33)
        yield from sea.watch(auto_driving.driveContinuous(drive, 0.1, math.pi/2, 0), shooter.dropGenerator())
        yield from sea.timeLimit(auto_driving.driveDistance(drive, -55, -0.33), 50)

        # cross the line...
        yield from auto_driving.driveDistance(drive, 35, .3)
        rotationTracker.setTargetOffsetRotation(-90)
        yield from auto_driving.driveDistance(drive, 100, .4)
        rotationTracker.setTargetOffsetRotation(0)
        yield from auto_driving.driveDistance(drive, 60, .33)

def shootFinal(drive, shooter, rotationTracker):
    yield from sea.watch(
        auto_driving.driveContinuous(drive, .1, math.pi/2, 0),
        shooter.shootGenerator())
    yield from auto_driving.driveDistance(drive, -25, -.5)
    # rotationTracker.setTargetOffsetRotation(
    #     rotationTracker.targetOffsetRotation + 180)
    # yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)


def autonomous(drive, ahrs, vision, shooter):
    multiDrive = sea.MultiDrive(drive)
    rotationTracker = auto_navx.RotationTracker(multiDrive, ahrs)
    rotationTracker.resetOrigin()
    rotationTracker.setTargetOffsetRotation(0)
    yield from sea.parallel(
        rotationTracker.rotateToTarget(),autoSequence(multiDrive, vision, rotationTracker, shooter),auto_driving.updateMultiDrive(multiDrive))
