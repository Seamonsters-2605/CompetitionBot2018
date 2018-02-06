import math
import ctre
import auto_commands
import strafe_to_align
import auto_shoot
import seamonsters as sea
import rotation_align
from robotpy_ext.common_drivers.navx import AHRS

def autoSequence(drive, vision):
    for i in range(70):
        drive.drive(.3, math.pi/2, 0)
        yield
    drive.drive(0, 0, 0)
    yield from sea.wait(25)
    for i in range(75):
        drive.drive(.3, 0, 0)
        yield
    drive.drive(0, 0, 0)
    yield from sea.wait(25)
    yield from sea.ensureTrue(strafe_to_align.strafeAlign(drive, vision, 0), 20)
    yield from sea.watch(sea.wait(50), strafe_to_align.strafeAlign(drive, vision, 0),
                         auto_commands.driveContinuous(drive, .2, math.pi/2, 0))

def autonomous(drive, ahrs, vision):
    multiDrive = sea.MultiDrive(drive)
    yield from sea.parallel(rotation_align.rotation(multiDrive, ahrs),
                            autoSequence(multiDrive, vision), auto_commands.updateMultiDrive(multiDrive))


    #yield from sea.watch(auto_commands.driveForward(drive, 49, .5), strafe_to_align.strafeAlign(drive, vision, 10))
    #yield from auto_shoot.Shooter.shootMotor(1, 200)

