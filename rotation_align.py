import ctre
from robotpy_ext.common_drivers.navx import AHRS

def rotation(drive, ahrs):
    startAngle = ahrs.getAngle()
    print("AAAAAAAA")
    while True:
        offset = ahrs.getAngle() - startAngle
        drive.drive(0, 0, offset/50)
        yield
