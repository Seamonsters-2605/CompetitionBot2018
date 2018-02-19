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

    strategy = None
    for strat in auto_strategies.STRATEGIES:
        switchName = switchPosition + " " + strat
        if sea.getSwitch(switchName, False):
            strategy = strat
    if strategy is None:
        strategy = auto_strategies.STRAT_CROSSLINE

    print("Location:", location)
    print("Switch position:", switchPosition)
    print("Strategy:", strategy)

    stratGenerator = auto_strategies.LOCATION_STRATEGIES[location]\
        [switchPosition][strategy]
    yield from stratGenerator(drive, rotationTracker)

    if strategy == auto_strategies.STRAT_SWITCHFRONT:
        yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
        if (yield from auto_vision.waitForVision(vision)):
            yield from sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0),
                                      20)
        else:
            print("Couldn't find vision!")
        drive.drive(0, 0, 0)
        yield from sea.timeLimit(auto_driving.driveDistance(drive, 53, .5), 50)
        drive.drive(0, 0, 0)
        yield from sea.watch(
            auto_driving.driveContinuous(drive, .1, math.pi/2, 0),
            shooter.shootGenerator())

    if strategy == auto_strategies.STRAT_SWITCHSIDE:
        yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
        yield from sea.timeLimit(auto_driving.driveDistance(drive, 30, .5), 50)
        drive.drive(0, 0, 0)
        yield from sea.watch(
            auto_driving.driveContinuous(drive, .1, math.pi/2, 0),
            shooter.shootGenerator())
        if switchPosition[0] == "L":
            yield from auto_strategies.left_switchSide_pickUpCube(drive, rotationTracker, shooter)
        if switchPosition[0] == "R":
            yield from auto_strategies.right_switchSide_pickUpCube(drive, rotationTracker, shooter)

    if strategy == auto_strategies.STRAT_EXCHANGE:
        yield from shooter.shootGenerator()
        yield from sea.timeLimit(auto_driving.driveDistance(drive, 25, 0.33),
                                 50)
        yield from auto_driving.driveDistance(drive, -35, -0.33)

def autonomous(drive, ahrs, vision, shooter):
    multiDrive = sea.MultiDrive(drive)
    rotationTracker = auto_navx.RotationTracker(multiDrive, ahrs)
    rotationTracker.resetOrigin()
    rotationTracker.setTargetOffsetRotation(0)
    yield from sea.parallel(
        rotationTracker.rotateToTarget(),autoSequence(multiDrive, vision, rotationTracker, shooter),auto_driving.updateMultiDrive(multiDrive))
