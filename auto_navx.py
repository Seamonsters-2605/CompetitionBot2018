ROTATE_SCALE = 1 / 220
ROTATE_EXPONENT = 0.7

class RotationTracker:

    def __init__(self, drive, ahrs):
        self.ahrs = ahrs
        self.drive = drive
        self.targetOffsetRotation = 0
        self.origin = 0

    def resetOrigin(self):
        try:
            self.origin = self.ahrs.getAngle()
        except ZeroDivisionError:
            print("well it looks like something's wrong with the NavX :(")
            self.targetOffsetRotation = 999999  # break NavX

    def setTargetOffsetRotation(self, value):
        self.targetOffsetRotation = value

    def rotateToTarget(self):
        while True:
            try:
                offset = self.ahrs.getAngle() - self.origin - self.targetOffsetRotation
            except ZeroDivisionError:
                print("well it looks like something's wrong with the NavX :(")
                self.targetOffsetRotation = 999999  # break NavX
            if abs(offset) > 360:
                print("NavX is broken!!")
                yield
                continue
            if offset > 0:
                driveSpeed = (offset * ROTATE_SCALE) ** ROTATE_EXPONENT
            else:
                driveSpeed = -(-offset * ROTATE_SCALE) ** ROTATE_EXPONENT
            self.drive.drive(0, 0, driveSpeed)
            yield

    def waitRotation(self, range):
        i = 0
        while True:
            i += 1
            if i > 5 * 50:
                self.targetOffsetRotation = 999999 # break NavX

            try:
                offset = self.ahrs.getAngle() - self.origin - self.targetOffsetRotation
            except ZeroDivisionError:
                print("well it looks like something's wrong with the NavX :(")
                self.targetOffsetRotation = 999999  # break NavX
            yield abs(offset) <= range

