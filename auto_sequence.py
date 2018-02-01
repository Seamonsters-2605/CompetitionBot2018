import auto_commands

def autoSequence(drive, vision):
    yield from auto_commands.driveForward(drive, 3*12, 0.1)
