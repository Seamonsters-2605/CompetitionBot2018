
def rotation(drive, ahrs, rotation=0):
    startAngle = ahrs.getAngle() + rotation
    while True:
        offset = ahrs.getAngle() - startAngle
        drive.drive(0, 0, offset/75)
        yield
