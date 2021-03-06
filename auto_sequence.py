import math
import auto_driving
import auto_vision
import auto_pauses
import seamonsters as sea
import auto_navx
import wpilib
import auto_strategies
import auto_override


def autoSequence(drive, vision, rotationTracker, shooter):
    shooter.stop()  # it sometimes is running when auto starts?

    gameMessage = wpilib.DriverStation.getInstance().getGameSpecificMessage()
    if gameMessage is None or gameMessage == "":
        switchPosition = "ERROR!"  # will cause it to default to CROSSLINE
    else:
        switchPosition = gameMessage[0]

    startPos = auto_override.override()

    table = sea.getNum()
    print('lpause is ',table['lpause'])
    print('rpause is ', table['rpause'])

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
        stratGenerator = auto_strategies.LOCATION_STRATEGIES[startPos] \
            [switchPosition][strategy]
    except KeyError:
        print("You chose an invalid auto sequence! Defaulting to Cross line")
        strategy = auto_strategies.STRAT_CROSSLINE
        stratGenerator = auto_strategies.LOCATION_STRATEGIES[startPos] \
            [switchPosition][strategy]

    yield from stratGenerator(drive, rotationTracker)

    if strategy == auto_strategies.STRAT_SWITCHFRONT:
        yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
        if not sea.getSwitch("Auto: Switch vision", False):
            print("Skipping vision")
        elif (yield from auto_vision.waitForVision(vision)):
            yield from sea.timeLimit(sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0),
                                                    20), 100)
        else:
            print("Couldn't find vision!")

        drive.drive(0, 0, 0)
        # for center autos: yield from sea.timeLimit(auto_driving.driveDistance(drive, 35, .5), 50)
        # for side autos:
        yield from sea.timeLimit(auto_driving.driveDistance(drive, 40, .5), 50)
        drive.drive(0, 0, 0)
        yield from shootFinal(drive, shooter, rotationTracker)
        if switchPosition == "R":
            yield from auto_strategies.right_RightCubePickup(drive, vision, shooter, rotationTracker)
            yield from auto_strategies.auto_SecondSwitchRight(drive, vision, shooter, rotationTracker)

        if switchPosition == "L":
            yield from auto_strategies.left_LeftCubePickup(drive, vision, shooter, rotationTracker)
            yield from auto_strategies.auto_SecondSwitchLeft(drive, vision, shooter, rotationTracker)

    if strategy == auto_strategies.STRAT_SWITCHSIDE:
        yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
        yield from sea.timeLimit(auto_driving.driveDistance(drive, 30, .4), 80)
        drive.drive(0, 0, 0)
        yield from shootFinal(drive, shooter, rotationTracker)

        if switchPosition == 'R':
            yield from auto_pauses.RightPause()
            yield from auto_strategies.right_backCube(drive, rotationTracker, shooter, vision)
        if switchPosition == 'L':
            yield from auto_pauses.LeftPause()
            yield from auto_strategies.left_backCube(drive, rotationTracker, shooter, vision)

    if strategy == auto_strategies.STRAT_EXCHANGE:
        yield from auto_driving.driveDistance(drive, -10, -.33)
        yield from sea.timeLimit(shooter.dropWhileDrivingGenerator(drive), 70)
        yield from sea.timeLimit(auto_driving.driveDistance(drive, -55, -0.33), 50)

        # cross the line...
        yield from auto_driving.driveDistance(drive, 35, .3)
        rotationTracker.setTargetOffsetRotation(-90)
        yield from auto_driving.driveDistance(drive, 100, .4)
        rotationTracker.setTargetOffsetRotation(0)
        yield from auto_driving.driveDistance(drive, 60, .33)


def shootFinal(drive, shooter, rotationTracker):
    yield from sea.watch(
        auto_driving.driveContinuous(drive, .1, math.pi / 2, 0),
        shooter.shootGenerator())
    yield from auto_driving.driveDistance(drive, -10, -.5)

    # rotationTracker.setTargetOffsetRotation(
    #     rotationTracker.targetOffsetRotation + 180)
    # yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)


def autonomous(drive, ahrs, vision, shooter):
    multiDrive = sea.MultiDrive(drive)
    rotationTracker = auto_navx.RotationTracker(multiDrive, ahrs)
    rotationTracker.resetOrigin()
    rotationTracker.setTargetOffsetRotation(0)
    yield from sea.parallel(
        rotationTracker.rotateToTarget(), autoSequence(multiDrive, vision, rotationTracker, shooter),
        auto_driving.updateMultiDrive(multiDrive),
        shooter.prepGenerator())
