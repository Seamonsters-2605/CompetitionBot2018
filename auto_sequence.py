import math
import ctre
import auto_commands
import auto_vision
import auto_shoot
import seamonsters as sea
import auto_navx
import wpilib
from robotpy_ext.common_drivers.navx import AHRS

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
    for i in range(60):
        drive.drive(.3, math.pi/2, 0)
        yield
    drive.drive(0, 0, 0)
   # yield from sea.watch(sea.untilTrue(auto_commands.watchWheelRotation(
    #    drive.interface.wheelMotors[sea.HolonomicDrive.FRONT_RIGHT], 70)),
     #                    auto_commands.driveContinuous(drive, .3, math.pi/2, 0))
    yield from sea.wait(25)
    if wpilib.DriverStation.getInstance().getLocation() == 1:
        for i in range(switchPos1):
            drive.drive(.3, 0, 0)
            yield
        drive.drive(0, 0, 0)
    elif wpilib.DriverStation.getInstance().getLocation() == 2:
        if switchPos2 == 75:
            for i in range(switchPos2):
                drive.drive(i/150, 0, 0)
                yield
        elif switchPos2 == 120:
            for i in range(switchPos2):
                drive.drive(-i/240, 0, 0)
                yield
        drive.drive(0, 0, 0)
    elif wpilib.DriverStation.getInstance().getLocation() == 3:
        for i in range(switchPos3):
            drive.drive(-.3, 0, 0)
            yield
        drive.drive(0, 0, 0)
    yield from sea.wait(25)
    yield from sea.ensureTrue(auto_vision.strafeAlign(drive, vision, 0), 20)
    drive.drive(0, 0, 0)
    yield from sea.watch(auto_vision.strafeAlign(drive, vision, 0),
                         auto_commands.driveContinuous(drive, .3, math.pi/2, 0), sea.wait(90))
    drive.drive(0, 0, 0)

def autonomous(drive, ahrs, vision):
    multiDrive = sea.MultiDrive(drive)
    yield from sea.parallel(auto_navx.rotation(multiDrive, ahrs),
                            autoSequence(multiDrive, vision), auto_commands.updateMultiDrive(multiDrive))


    #yield from sea.watch(auto_commands.driveForward(drive, 49, .5), strafe_to_align.strafeAlign(drive, vision, 10))
    #yield from auto_shoot.Shooter.shootMotor(1, 200)


def findTarget(vision, initialWait, timeLimit):
    yield from sea.wait(initialWait)
    yield from sea.timeLimit(
        sea.ensureTrue(auto_vision.checkForVisionTarget(vision), 25),
        timeLimit - initialWait)