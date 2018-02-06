import auto_commands
import strafe_to_align
import auto_shoot
import seamonsters as sea
import rotation_align
from robotpy_ext.common_drivers.navx import AHRS

def autoSequence(drive, vision, ahrs):
    yield from rotation_align.rotation(drive, ahrs)
    yield from auto_commands.driveForward(drive, 60, .5)
    yield from sea.wait(25)
    drive.resetTargetPosition()
    for i in range(50):
        drive.drive(.3, 0, 0)
        yield
    drive.drive(0, 0, 0)
    yield from sea.wait(25)
    yield from sea.untilTrue(strafe_to_align.strafeAlign(drive, vision, 10))
    yield from auto_commands.driveForward(drive, 49, .3)



    #yield from sea.watch(auto_commands.driveForward(drive, 49, .5), strafe_to_align.strafeAlign(drive, vision, 10))
    #yield from auto_shoot.Shooter.shootMotor(1, 200)