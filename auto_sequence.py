import auto_commands
import strafe_to_align
def autoSequence(drive, vision):
    yield from strafe_to_align.strafeAlign(drive,vision,10)