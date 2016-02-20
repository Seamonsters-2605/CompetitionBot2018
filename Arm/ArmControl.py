__author__ = "jacobvanthoog"
import wpilib
import math

TICKS_PER_ROTATION = 400
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

        self.Velocity = 80 # ticks per step

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

    def setVelocity(self, velocity):
        self.Velocity = velocity

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

        self.CAN1Target = self.can1RadiansToEncoderPosition(angle1)
        self.CAN2Target = self.can2RadiansToEncoderPosition(angle2)

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

    def ensureControlMode(self, can):
        if not (can.getControlMode() == wpilib.CANTalon.ControlMode.Position):
            can.changeControlMode(wpilib.CANTalon.ControlMode.Position)

    def radiansToEncoderPosition(self, radians, zero, offset, invert):
        position = radians / (2*math.pi) * TICKS_PER_ROTATION
        position *= invert
        position -= zero
        position += offset
        return math.floor(position)

    def can1RadiansToEncoderPosition(self, radians):
        return self.radiansToEncoderPosition(radians,
                                             self.CAN1Zero,
                                             self.CAN1Offset,
                                             self.CAN1Invert)

    def can2RadiansToEncoderPosition(self, radians):
        return self.radiansToEncoderPosition(radians,
                                             self.CAN2Zero,
                                             self.CAN2Offset,
                                             self.CAN2Invert)

    def rotateToPosition(self, can, target):
        current = can.getEncPosition();
        if current == target:
            return

        distance = target - current # amount motor should rotate
        if distance > TICKS_PER_ROTATION/2: # can rotate backwards instead
            distance = -TICKS_PER_ROTATION + distance

        # limit rotation to maximum velocity
        if distance > self.Velocity:
            distance = self.Velocity
        if distance < -self.Velocity:
            distance = -self.Velocity

        can.set(current + distance)

    def canMovementCompleted(self, can, target):
        return abs(can.getEncPosition() - target) <= COMPLETED_DISTANCE