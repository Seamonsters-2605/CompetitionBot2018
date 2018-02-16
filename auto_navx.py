
def rotation(drive, ahrs, angleHolder=None):
    if angleHolder == None:
        angleHolder = [0.0]
    startAngle = ahrs.getAngle()
    while True:
        offset = ahrs.getAngle() - startAngle - angleHolder[0]
        drive.drive(0, 0, offset/100)
        yield
