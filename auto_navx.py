
def rotation(drive, ahrs, angleHolder=None):
    if angleHolder == None:
        angleHolder = [0.0]
    startAngle = ahrs.getAngle()
    while True:
        offset = ahrs.getAngle() - angleHolder[0]
        drive.drive(0, 0, offset/75)
        yield
