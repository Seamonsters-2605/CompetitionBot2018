import math
import auto_driving
import auto_vision
import seamonsters as sea
import auto_navx
import wpilib
from auto_strategies import *



def autoSequence(drive, vision):

    vision.getEntry('camMode').setNumber(0)

    switchPosition = wpilib.DriverStation.getInstance().getGameSpecificMessage()
    startPosition =  wpilib.DriverStation.getInstance().getLocation()
    if len(switchPosition) == 0:
        print("No game message!")
        return

    if not sea.getSwitch("Activate Switch", False):
        attempt_switch = switchPosition[0]
    else:
        attempt_switch = "cross" + switchPosition[0]

    start_l = {"L": left_left, "R": left_right, "crossL":left_cross, "crossR":left_cross}
    start_m = {"L": mid_left, "R": mid_right, "crossR": mid_cross_right,"crossL": mid_cross_left}
    start_r = {"L": right_left, "R": right_right, "crossL":right_cross, "crossR": right_cross}

    targets = [start_l, start_m, start_r]
    drive_func = targets[startPosition - 1][attempt_switch]
    drive_func(drive)

    #align with vision
    yield from sea.wait(25)
    yield from sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0), 20)
    drive.drive(0, 0, 0)
    yield from sea.watch(auto_vision.strafeAlign(drive, vision, 0),
                         auto_driving.driveContinuous(drive, .3, math.pi / 2, 0), sea.wait(90))
    drive.drive(0, 0, 0)


def autonomous(drive, ahrs, vision, shooter):
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