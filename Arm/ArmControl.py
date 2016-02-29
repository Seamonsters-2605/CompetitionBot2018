__author__ = "jacobvanthoog"
import wpilib
import math

ROTATION_TICKS_CAN1 = 131072 # encoder ticks in a full rotation
ROTATION_TICKS_CAN2 = 756
MAGNITUDE_LIMIT = 1 # units before theoretical maximum distance
COMPLETED_DISTANCE = 5 # when both motors are within this number of ticks, the
                       # movement has completed

class ArmControl:

    # can1 is the motor at the base of the arm
    # can2 is the motor at the joint1
    def __init__(self, can1, can2):
        self.CAN1 = can1
        self.CAN2 = can2
        self.ensureControlMode(self.CAN1)
        self.ensureControlMode(self.CAN2)
        self.Length1 = 17.5
        self.Length2 = 20.0
        self.CAN1Offset = 0 # rotation offset, in encoder ticks
        self.CAN2Offset = 0
        self.CAN1Invert = 1 # can be 1 or -1 (inverted)
        self.CAN2Invert = 1
        self.zeroEncoders()

        # target position of the encoders
        # the zero, offset, and inverts should have already been factored in
        self.CAN1Target = self.CAN1.getEncPosition()
        self.CAN2Target = self.CAN2.getEncPosition()

        self.CAN1Velocity = 16384 # ticks per step
        self.CAN2Velocity = 80

        self.MovementCompleted = False


    # should be called once per loop!
    def update(self):
        self.rotateToPosition(self.CAN1, self.CAN1Target)
        self.rotateToPosition(self.CAN2, self.CAN2Target)
        self.MovementCompleted = \
            self.canMovementCompleted(self.CAN1, self.CAN1Target) and \
            self.canMovementCompleted(self.CAN2, self.CAN2Target)


    def zeroEncoders(self):
        self.CAN1Zero = self.CAN1.getEncPosition()
        self.CAN2Zero = self.CAN2.getEncPosition()

    def invert1(self, invert = True):
        self.CAN1Invert = -1 if invert else 1

    def invert2(self, invert = True):
        self.CAN2Invert = -1 if invert else 1

    # set the rotation offset of encoders -- specified in encoder ticks

    def setOffset1(self, offset):
        self.CAN1Offset = offset

    def setOffset2(self, offset):
        self.CAN2Offset = offset

    def setVelocity1(self, velocity):
        self.CAN1Velocity = velocity

    def setVelocity2(self, velocity):
        self.CAN2Velocity = velocity

    # mag is distance from the base of the arm, in inches
    # dir is the angle of the target point, where 0 is straight ahead and Pi/2
    # is straight up
    # The end of the arm will attempt to move to the point defined by these
    # values
    def moveTo(self, mag, dir):
        dir %= 2 * math.pi # constrain dir to be between 0 and 2pi
        if mag > self.Length1 + self.Length2 - MAGNITUDE_LIMIT:
            mag = self.Length1 + self.Length2 - MAGNITUDE_LIMIT
        if mag < abs(self.Length1 + self.Length2):
            mag = abs(self.Length1 + self.Length2)
        angle1 = math.acos( -(self.Length2**2 - self.Length1**2 - mag**2)
                            / (2 * self.Length1 * mag)) + dir
        angle2 = math.acos( -(mag**2 - self.Length1**2 - self.Length2**2)
                            / (2 * self.Length1 * self.Length2))

        self.CAN1Target = self.radiansToEncoderPosition(angle1, self.CAN1)
        self.CAN2Target = self.radiansToEncoderPosition(angle2, self.CAN2)

    # variant of moveTo() that is given a position
    # x is forward distance from the base of the arm, in inches
    # y is upward distance
    def moveToPosition(self, x, y):
        mag = math.sqrt(x**2 + y**2)
        dir = math.atan2(y, x)
        self.moveTo(mag, dir)

    def movementCompleted(self):
        return self.MovementCompleted


    # DON'T USE THESE

    def ticksPerRotation(self, can):
        if can == self.CAN1:
            return ROTATION_TICKS_CAN1
        if can == self.CAN2:
            return ROTATION_TICKS_CAN2
        return None

    def inverted(self, can):
        if can == self.CAN1:
            return self.CAN1Invert
        if can == self.CAN2:
            return self.CAN2Invert
        return None

    def zero(self, can):
        if can == self.CAN1:
            return self.CAN1Zero
        if can == self.CAN2:
            return self.CAN2Zero
        return None

    def offset(self, can):
        if can == self.CAN1:
            return self.CAN1Offset
        if can == self.CAN2:
            return self.CAN2Offset
        return None

    def target(self, can):
        if can == self.CAN1:
            return self.CAN1Target
        if can == self.CAN2:
            return self.CAN2Target
        return None

    def velocity(self, can):
        if can == self.CAN1:
            return self.CAN1Velocity
        if can == self.CAN2:
            return self.CAN2Velocity
        return None

    def ensureControlMode(self, can):
        if not (can.getControlMode() == wpilib.CANTalon.ControlMode.Position):
            can.changeControlMode(wpilib.CANTalon.ControlMode.Position)

    def radiansToEncoderPosition(self, radians, can):
        position = radians / (2*math.pi) * self.ticksPerRotation(can)
        position *= self.inverted(can)
        position -= self.zero(can)
        position += self.offset(can)
        return math.floor(position)

    def rotateToPosition(self, can, target):
        current = can.getEncPosition()
        if current == target:
            return

        distance = target - current # amount motor should rotate
        if distance > self.ticksPerRotation(can)/2: # can rotate backwards instead
            distance -= self.ticksPerRotation(can)

        # limit rotation to maximum velocity
        if distance > self.velocity(can):
            distance = self.velocity(can)
        if distance < -self.velocity(can):
            distance = -self.velocity(can)

        can.set(current + distance)

    def canMovementCompleted(self, can, target):
        return abs(can.getEncPosition() - target) <= COMPLETED_DISTANCE