import auto_commands
import strafe_to_align
import auto_shoot
import seamonsters as sea
def autoSequence(drive, vision):
    yield from auto_commands.driveForward(drive, 60, .5)
    for i in range(50):
        drive.drive(.5, 0, 0)
        yield
    drive.drive(0, 0, 0)
    yield from sea.watch(auto_commands.driveForward(drive, 49, .5), strafe_to_align.strafeAlign(drive, vision, 10))
    yield from auto_shoot.Shooter.shootMotor(1, 200)