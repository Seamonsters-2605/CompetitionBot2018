ROTATE_SCALE = 1 / 220
ROTATE_EXPONENT = 0.7

class RotationTracker:

    def __init__(self, drive, ahrs):
        self.ahrs = ahrs
        self.drive = drive
        self.targetOffsetRotation = 0
        self.origin = 0

    def resetOrigin(self):
        self.origin = self.ahrs.getAngle()

    def setTargetOffsetRotation(self, value):
        self.targetOffsetRotation = value

    def rotateToTarget(self):
        while True:
            offset = self.ahrs.getAngle() - self.origin - self.targetOffsetRotation
            if offset > 0:
                driveSpeed = (offset * ROTATE_SCALE) ** ROTATE_EXPONENT
            else:
                driveSpeed = -(-offset * ROTATE_SCALE) ** ROTATE_EXPONENT
            self.drive.drive(0, 0, driveSpeed)
            yield

    def waitRotation(self, range):
        while True:
            offset = self.ahrs.getAngle() - self.origin - self.targetOffsetRotation
            yield abs(offset) <= range
