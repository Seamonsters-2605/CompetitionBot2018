import math
import ctre
import seamonsters as sea
from seamonsters import HolonomicDrive
import robotconfig

def driveContinuous(drive, magnitude, direction, turn):
    try:
        while True:
            drive.drive(magnitude, direction, turn)
            yield
    except:
        drive.drive(0, 0, 0)

def driveDistance(drive, distance, speed, dualMotor=False):
    if sea.getSwitch("Drive voltage mode", False):
        yield from sea.timeLimit(driveContinuous(drive, speed, math.pi/2, 0),
                                 abs(int(distance*0.75)))
        drive.drive(0, 0, 0)
        return
    holoDrive = _findTheHoloDrive(drive)
    motor1 = holoDrive.wheelMotors[HolonomicDrive.FRONT_RIGHT]
    motor2 = holoDrive.wheelMotors[HolonomicDrive.FRONT_LEFT]
    moveTicks = int(float(distance) * robotconfig.ticksPerWheelRotation
                     / robotconfig.wheelCircumference * holoDrive.invert)
    def motorPos():
        if dualMotor:
            return int((motor1.getSelectedSensorPosition(0)
                   - motor2.getSelectedSensorPosition(0)) / 2)
        else:
            return motor1.getSelectedSensorPosition(0)
    targetPosition = motorPos() + moveTicks
    def checkTheMotor():
        yield
        while True:
            pos = motorPos()
            if moveTicks > 0:
                if pos >= targetPosition:
                    break
                else:
                    yield
            else:
                if pos <= targetPosition:
                    break
                else:
                    yield
    yield from sea.watch(driveContinuous(drive, speed, math.pi/2, 0),
                         checkTheMotor())

def _findTheHoloDrive(drive):
    if isinstance(drive, HolonomicDrive):
        return drive
    else:
        try:
            return _findTheHoloDrive(drive.interface)
        except AttributeError:
            raise TypeError("Not a HolonomicDrive or wrapper!")


def updateMultiDrive(multiDrive):
    while True:
        multiDrive.update()
        yield

def driveForward(holoDrive, distance, speed):
    holoDrive = _findTheHoloDrive(holoDrive)
    wheelMotors = holoDrive.wheelMotors
    speed *= robotconfig.maxVelocityPositionMode
    moveTicks = int(float(distance) * robotconfig.ticksPerWheelRotation
                / robotconfig.wheelCircumference * holoDrive.invert)

    currentTargets = []
    targetPositions = []
    for i in range(0, 4):
        motor = wheelMotors[i]
        currentPos = motor.getSelectedSensorPosition(0)
        if i == HolonomicDrive.FRONT_RIGHT or i == HolonomicDrive.BACK_RIGHT:
            targetPos = currentPos + moveTicks
        else:
            targetPos = currentPos - moveTicks
        currentTargets.append(currentPos)
        targetPositions.append(targetPos)

    while True:
        yield
        done = True
        for i in range(0, 4):
            motor = wheelMotors[i]
            target = targetPositions[i]
            current = currentTargets[i]
            if abs(target - current) < speed:
                current = target
            else:
                if target > current:
                    current += speed
                else:
                    current -= speed
            if target != current:
                done = False
            if abs(motor.getSelectedSensorPosition(0) - target) > speed * 2:
                done = False
            currentTargets[i] = current
            motor.set(ctre.ControlMode.Position, current)
        if done:
            break

def driveToTargetDistance(drive, vision):
    # each vision target strip is 16x2 in, with a 4in gap (64 in accurate area)
    targetRealArea = 64

    # experimental focal distance
    focalDist = 600

    perceivedArea = vision.getNumber('ta','borked')

    distance = focalDist * (targetRealArea ** 0.5) / (perceivedArea ** 0.5)
