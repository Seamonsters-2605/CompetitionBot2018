
import ctre
import auto_commands
import strafe_to_align
def autoSequence(drive, vision):
    drive.setDriveMode(ctre.ControlMode.Position)
    yield from strafe_to_align.strafeAlign(drive,vision,0)