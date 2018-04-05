import math
import auto_driving
import auto_vision
import auto_pauses
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
STRATEGIES = [STRAT_NONE, STRAT_CROSSLINE, STRAT_SWITCHFRONT, STRAT_SWITCHSIDE,
              STRAT_EXCHANGE]

# Names: start location, switch direction, strategy


def doNothing(drive, rotationTracker):
    yield

def loc1_left_switchFront(drive, rotationTracker):
    print("running loc1_left_switchFront")
    yield from auto_driving.driveDistance(drive, 15, .33)
    rotationTracker.setTargetOffsetRotation(45)
    yield from auto_pauses.LeftPause()
    yield from auto_driving.driveDistance(drive, 42, .33)
    rotationTracker.setTargetOffsetRotation(0)

def loc1_right_switchFront(drive, rotationTracker):
    print("running loc1_right_switchFront")
    yield from auto_driving.driveDistance(drive, 10, .33)
    rotationTracker.setTargetOffsetRotation(80)
    yield from auto_pauses.RightPause()
    yield from auto_driving.driveDistance(drive, 115, .45)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0,0,0)

def loc1_crossLine(drive, rotationTracker):
    print("running loc1_crossLine")
    yield from auto_driving.driveDistance(drive, 20, .45)
    rotationTracker.setTargetOffsetRotation(-20)
    yield from auto_driving.driveDistance(drive, 70, .45)
    rotationTracker.setTargetOffsetRotation(0)
    yield from auto_driving.driveDistance(drive, 50, .33)

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
    yield from auto_driving.driveDistance(drive, 15, .45)
    rotationTracker.setTargetOffsetRotation(-65)
    yield from auto_pauses.LeftPause()
    yield from auto_driving.driveDistance(drive, 100, .45)
    rotationTracker.setTargetOffsetRotation(0)

def loc2_right_switchFront(drive, rotationTracker):
    print("running loc2_right_switchFront")
    yield from auto_driving.driveDistance(drive, 15, .45)
    rotationTracker.setTargetOffsetRotation(45)
    yield from auto_pauses.RightPause()
    yield from auto_driving.driveDistance(drive, 42, .45)
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
    yield from auto_driving.driveDistance(drive, 10, .40)
    rotationTracker.setTargetOffsetRotation(-80)
    yield from auto_pauses.LeftPause()
    yield from auto_driving.driveDistance(drive, 170, .45)
    rotationTracker.setTargetOffsetRotation(0)

def loc3_right_switchFront(drive, rotationTracker):
    print("running loc3_right_switchFront")
    yield from auto_driving.driveDistance(drive, 15, .33)
    rotationTracker.setTargetOffsetRotation(-45)
    yield from auto_pauses.RightPause()
    yield from auto_driving.driveDistance(drive, 57, .33)
    rotationTracker.setTargetOffsetRotation(0)

def loc3_crossLine(drive, rotationTracker):
    print("running loc1_crossLine")
    yield from auto_driving.driveDistance(drive, 20, .45)
    rotationTracker.setTargetOffsetRotation(20)
    yield from auto_driving.driveDistance(drive, 70, .45)
    rotationTracker.setTargetOffsetRotation(0)
    yield from auto_driving.driveDistance(drive, 50, .33)

def loc3_right_switchSide(drive, rotationTracker):
    print("running loc3_right_switchSide")
    yield from loc3_crossLine(drive, rotationTracker)
    rotationTracker.setTargetOffsetRotation(-90)

def right_backCube(drive, rotationTracker, shooter, vision):
    print("running right_backCube")
    rotationTracker.setTargetOffsetRotation(-180)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, -50, -.33)
    rotationTracker.setTargetOffsetRotation(-90)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, 60, .33)
    rotationTracker.setTargetOffsetRotation(0)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    #yield from sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0), 20)
    yield from sea.timeLimit(sea.watch(shooter.shootGenerator(), auto_driving.driveDistance(drive, -30, -.33)), 150)
    yield from auto_driving.driveDistance(drive, 10, .33)
    rotationTracker.setTargetOffsetRotation(180)
    yield from sea.timeLimit(sea.ensureTrue(rotationTracker.waitRotation(5), 20), 100)
    yield from auto_driving.driveDistance(drive, 25, .33)
    yield from sea.watch(
        auto_driving.driveContinuous(drive, .1, math.pi / 2, 0),
        shooter.shootGenerator())
    yield from auto_driving.driveDistance(drive, -25, -.5)

def left_backCube(drive, rotationTracker, shooter, vision):
    rotationTracker.setTargetOffsetRotation(180)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, -50, -.33)
    rotationTracker.setTargetOffsetRotation(90)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, 50, .33)
    rotationTracker.setTargetOffsetRotation(0)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    #yield from sea.timeLimit(sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0), 20), 100)
    yield from sea.timeLimit(sea.watch(shooter.shootGenerator(), auto_driving.driveDistance(drive, -30, -.33)), 150)
    yield from auto_driving.driveDistance(drive, 10, .33)
    rotationTracker.setTargetOffsetRotation(180)
    yield from sea.ensureTrue(rotationTracker.waitRotation(5), 20)
    yield from auto_driving.driveDistance(drive, 25, .33)
    yield from sea.watch(
        auto_driving.driveContinuous(drive, .1, math.pi / 2, 0),
        shooter.shootGenerator())
    yield from auto_driving.driveDistance(drive, -25, -.5)

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
    },
    SWITCH_RIGHT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc1_crossLine,
        STRAT_SWITCHFRONT: loc1_right_switchFront,
        STRAT_EXCHANGE: loc1_exchange,

    }
}

LOCATION2_STRATEGIES = {
    SWITCH_LEFT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc2_left_crossLine,
        STRAT_SWITCHFRONT: loc2_left_switchFront,
        STRAT_SWITCHSIDE: loc2_left_switchSide,
        STRAT_EXCHANGE: loc2_exchange,
    },
    SWITCH_RIGHT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc2_right_crossLine,
        STRAT_SWITCHFRONT: loc2_right_switchFront,
        STRAT_SWITCHSIDE: loc2_right_switchSide,
        STRAT_EXCHANGE: loc2_exchange,
    }
}

LOCATION3_STRATEGIES = {
    SWITCH_LEFT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc3_crossLine,
        STRAT_SWITCHFRONT: loc3_left_switchFront,
    },
    SWITCH_RIGHT: {
        STRAT_NONE: doNothing,
        STRAT_CROSSLINE: loc3_crossLine,
        STRAT_SWITCHFRONT: loc3_right_switchFront,
        STRAT_SWITCHSIDE: loc3_right_switchSide,
    }
}


LOCATION_STRATEGIES = [None,
                       LOCATION1_STRATEGIES,
                       LOCATION2_STRATEGIES,
                       LOCATION3_STRATEGIES]
