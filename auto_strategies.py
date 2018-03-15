import math
import auto_driving
import auto_vision
import seamonsters as sea
import auto_navx
import wpilib
import auto_vision
import shooter

SWITCH_LEFT = "L"
SWITCH_RIGHT = "R"

STRAT_NONE = "Do nothing"
STRAT_CROSSLINE = "Cross line"
STRAT_SWITCHFRONT = "Switch front"
STRAT_SWITCHSIDE = "Switch side"
STRAT_EXCHANGE = "Exchange"
STRAT_BACKCUBE = "Pick up back cube"
STRATEGIES = [STRAT_NONE, STRAT_CROSSLINE, STRAT_SWITCHFRONT, STRAT_SWITCHSIDE,
              STRAT_EXCHANGE, STRAT_BACKCUBE]

# Names: start location, switch direction, strategy


def doNothing(drive, rotationTracker):
    yield

def loc1_left_switchFront(drive, rotationTracker):
    print("running loc1_left_switchFront")
    yield from auto_driving.driveDistance(drive, 15, .33)
    rotationTracker.setTargetOffsetRotation(45)
    yield from auto_driving.driveDistance(drive, 47, .33)
    rotationTracker.setTargetOffsetRotation(0)

def loc1_right_switchFront(drive, rotationTracker):
    print("running loc1_right_switchFront")
    yield from auto_driving.driveDistance(drive, 40, .33)
    rotationTracker.setTargetOffsetRotation(90)
    yield from auto_driving.driveDistance(drive, 150, .45)
    rotationTracker.setTargetOffsetRotation(0)
    #yield from auto_driving.driveDistance(drive,70,.33)
    yield
    drive.drive(0,0,0)

def loc1_crossLine(drive, rotationTracker):
    print("running loc1_crossLine")
    yield from auto_driving.driveDistance(drive, 20, .7)
    rotationTracker.setTargetOffsetRotation(-20)
    yield from auto_driving.driveDistance(drive, 100, .7)
    rotationTracker.setTargetOffsetRotation(0)

def loc1_left_switchSide(drive, rotationTracker):
    print("running loc1_left_switchSide")
    yield from loc1_crossLine(drive, rotationTracker)
    rotationTracker.setTargetOffsetRotation(90)

def loc1_exchange(drive, rotationTracker):
    print("running loc1_exchange")
    yield from auto_driving.driveDistance(drive, 20, .33)
    yield from sea.timeLimit(auto_driving.driveContinuous(drive, 0, 0, 0), 10)
    rotationTracker.setTargetOffsetRotation(90)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, 50, .33)
    yield from sea.timeLimit(auto_driving.driveContinuous(drive, 0, 0, 0), 10)
    rotationTracker.setTargetOffsetRotation(0)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)

def loc2_left_switchFront(drive, rotationTracker):
    print("running loc2_left_switchFront")
    yield from auto_driving.driveDistance(drive, 35, .33)
    rotationTracker.setTargetOffsetRotation(-90)
    #yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive,100,.33)
    rotationTracker.setTargetOffsetRotation(0)

def loc2_right_switchFront(drive, rotationTracker):
    print("running loc2_right_switchFront")
    yield from auto_driving.driveDistance(drive, 12, .33)
    rotationTracker.setTargetOffsetRotation(45)
    yield from auto_driving.driveDistance(drive, 57, .33)
    rotationTracker.setTargetOffsetRotation(0)
    yield

def loc2_crossLine_start(drive, rotationTracker):
    yield from auto_driving.driveDistance(drive, 35, .3)

def loc2_left_crossLine(drive, rotationTracker):
    print("running loc2_left_crossLine")
    yield from loc2_crossLine_start(drive, rotationTracker)
    rotationTracker.setTargetOffsetRotation(90)
    yield from auto_driving.driveDistance(drive, 70, .6)
    rotationTracker.setTargetOffsetRotation(0)
    yield from auto_driving.driveDistance(drive, 120, .33)

def loc2_right_crossLine(drive, rotationTracker):
    print("running loc2_right_crossLine")
    yield from loc2_crossLine_start(drive, rotationTracker)
    rotationTracker.setTargetOffsetRotation(-90)
    yield from auto_driving.driveDistance(drive, 155, .4)
    rotationTracker.setTargetOffsetRotation(0)
    yield from auto_driving.driveDistance(drive, 60, .33)

def loc2_left_switchSide(drive, rotationTracker):
    print("running loc2_left_switchSide")
    yield from loc2_right_crossLine(drive, rotationTracker)
    rotationTracker.setTargetOffsetRotation(90)

def loc2_right_switchSide(drive, rotationTracker):
    print("running loc2_right_switchSide")
    yield from loc2_left_crossLine(drive, rotationTracker)
    rotationTracker.setTargetOffsetRotation(-90)

def loc2_exchange(drive, rotationTracker):
    print("running loc2_exchange")
    yield from auto_driving.driveDistance(drive, 20, .33)
    yield from sea.timeLimit(auto_driving.driveContinuous(drive, 0, 0, 0), 10)
    rotationTracker.setTargetOffsetRotation(-90)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, 33, .33)
    yield from sea.timeLimit(auto_driving.driveContinuous(drive, 0, 0, 0), 10)
    rotationTracker.setTargetOffsetRotation(0)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)

def loc3_left_switchFront(drive, rotationTracker):
    print("running loc3_left_switchFront")
    yield from auto_driving.driveDistance(drive, 35, .33)
    rotationTracker.setTargetOffsetRotation(-90)
    yield from auto_driving.driveDistance(drive, 200, .45)
    rotationTracker.setTargetOffsetRotation(0)

def loc3_right_switchFront(drive, rotationTracker):
    print("running loc3_right_switchFront")
    yield from auto_driving.driveDistance(drive, 15, .33)
    rotationTracker.setTargetOffsetRotation(-45)
    yield from auto_driving.driveDistance(drive, 57, .33)
    rotationTracker.setTargetOffsetRotation(0)

def loc3_crossLine(drive, rotationTracker):
    print("running loc1_crossLine")
    yield from auto_driving.driveDistance(drive, 20, .7)
    rotationTracker.setTargetOffsetRotation(20)
    yield from auto_driving.driveDistance(drive, 100, .7)
    rotationTracker.setTargetOffsetRotation(0)

def loc3_right_switchSide(drive, rotationTracker):
    print("running loc3_right_switchSide")
    yield from loc3_crossLine(drive, rotationTracker)
    rotationTracker.setTargetOffsetRotation(-90)

def right_backCube(drive, rotationTracker):
    print("running right_backCube")
    rotationTracker.setTargetOffsetRotation(180)
    yield from auto_driving.driveDistance(drive, -10, -.33)
    for i in range(200):
        drive.drive(.33, 0, 0)
        yield
    drive.drive(0, 0, 0)
    yield from auto_driving.driveDistance(drive, 10, .33)
    # pick up cube
    yield from auto_driving.driveDistance(drive, -10, .33)
    rotationTracker.setTargetOffsetRotation(0)

def left_backCube(drive, rotationTracker):
    print("running left_backCube")
    rotationTracker.setTargetOffsetRotation(180)
    yield from auto_driving.driveDistance(drive, -10, -.33)
    for i in range(200):
        drive.drive(-.33, 0, 0)
        yield
    drive.drive(0, 0, 0)
    yield from auto_driving.driveDistance(drive, 10, .33)
    # pick up cube
    yield from auto_driving.driveDistance(drive, -10, .33)
    rotationTracker.setTargetOffsetRotation(0)

def right_RightCubePickup(drive, vision, shooter,  rotationTracker):
    print("running right_frontCubePickup")
    yield from auto_driving.driveDistance(drive, -30, -.33)
    rotationTracker.setTargetOffsetRotation(-90)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, 50, .33)
    rotationTracker.setTargetOffsetRotation(-180)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    #vision
    if (yield from auto_vision.waitForVision(vision)):
        yield from sea.timeLimit(sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0),
                                                20), 100)
    else:
        print("Couldn't find vision!")
    #pick up cube
    yield from sea.watch(shooter.shootGenerator(), auto_driving.driveDistance(drive, -20, -.33))
    yield from auto_driving.driveDistance(drive, 25, .33)

def left_LeftCubePickup(drive, vision, shooter, rotationTracker):
    print("running left_LeftCubePickup")
    yield from auto_driving.driveDistance(drive, -30, -.33)
    rotationTracker.setTargetOffsetRotation(90)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, 50, .33)
    rotationTracker.setTargetOffsetRotation(-180)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    #vision
    if (yield from auto_vision.waitForVision(vision)):
        yield from sea.timeLimit(sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0),
                                                20), 100)
    else:
        print("Couldn't find vision!")
    #pick up cube
    yield from sea.watch(shooter.shootGenerator(), auto_driving.driveDistance(drive, -20, -.33))
    yield from auto_driving.driveDistance(drive, 25, .33)

def auto_CubeExchange(drive, shooter, rotationTracker):
    yield from auto_driving.driveDistance(drive, 10, .33)
    rotationTracker.setTargetOffsetRotation(-150)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, 65, .33)
    rotationTracker.setTargetOffsetRotation(-0)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from sea.timeLimit(shooter.dropWhileDrivingGenerator(drive), 70)
    yield from auto_driving.driveDistance(drive, -40, -.33)

def auto_SecondSwitchRight(drive, vision, shooter, rotationTracker):
    yield from auto_driving.driveDistance(drive, 25, .33)
    rotationTracker.setTargetOffsetRotation(45)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, 75, .33)
    rotationTracker.setTargetOffsetRotation(-0)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from sea.watch(shooter.shootGenerator(), auto_driving.driveDistance(drive, 35, .33),
                             sea.wait(50))

def auto_SecondSwitchLeft(drive, vision, shooter, rotationTracker):
    yield from auto_driving.driveDistance(drive, 25, .33)
    rotationTracker.setTargetOffsetRotation(-45)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, 75, .33)
    rotationTracker.setTargetOffsetRotation(-0)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from sea.watch(shooter.shootGenerator(), auto_driving.driveDistance(drive, 35, .33),
                             sea.wait(50))

LOCATION1_STRATEGIES = {
    SWITCH_LEFT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc1_crossLine,
        STRAT_SWITCHFRONT: loc1_left_switchFront,
        STRAT_SWITCHSIDE: loc1_left_switchSide,
        STRAT_EXCHANGE: loc1_exchange,
        STRAT_BACKCUBE: left_backCube
    },
    SWITCH_RIGHT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc1_crossLine,
        STRAT_SWITCHFRONT: loc1_right_switchFront,
        STRAT_EXCHANGE: loc1_exchange,
        STRAT_BACKCUBE: right_backCube

    }
}

LOCATION2_STRATEGIES = {
    SWITCH_LEFT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc2_left_crossLine,
        STRAT_SWITCHFRONT: loc2_left_switchFront,
        STRAT_SWITCHSIDE: loc2_left_switchSide,
        STRAT_EXCHANGE: loc2_exchange,
        STRAT_BACKCUBE: left_backCube
    },
    SWITCH_RIGHT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc2_right_crossLine,
        STRAT_SWITCHFRONT: loc2_right_switchFront,
        STRAT_SWITCHSIDE: loc2_right_switchSide,
        STRAT_EXCHANGE: loc2_exchange,
        STRAT_BACKCUBE: right_backCube
    }
}

LOCATION3_STRATEGIES = {
    SWITCH_LEFT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc3_crossLine,
        STRAT_SWITCHFRONT: loc3_left_switchFront,
        STRAT_BACKCUBE: left_backCube
    },
    SWITCH_RIGHT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc3_crossLine,
        STRAT_SWITCHFRONT: loc3_right_switchFront,
        STRAT_SWITCHSIDE: loc3_right_switchSide,
        STRAT_BACKCUBE: right_backCube
    }
}


LOCATION_STRATEGIES = [None,
                       LOCATION1_STRATEGIES,
                       LOCATION2_STRATEGIES,
                       LOCATION3_STRATEGIES]
