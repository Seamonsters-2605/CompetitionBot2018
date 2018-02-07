import ctre
from seamonsters import HolonomicDrive
import robotconfig
from networktables import NetworkTables

def driveContinuous(drive, magnitude, direction, turn):
    try:
        while True:
            drive.drive(magnitude, direction, turn)
            yield
    except:
        drive.drive(0, 0, 0)

def updateMultiDrive(multiDrive):
    while True:
        multiDrive.update()
        yield

def watchWheelRotation(motor, distance):
    moveTicks = int(float(distance) * robotconfig.ticksPerWheelRotation
                    / robotconfig.wheelCircumference)
    targetPosition = motor.getSelectedSensorPosition(0) + moveTicks
    while True:
        pos = motor.getSelectedSensorPosition(0)
        if moveTicks > 0:
            yield pos >= targetPosition
        else:
            yield pos <= targetPosition

def driveForward(holoDrive, distance, speed):
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

    print("Moving", moveTicks)

    while True:
        yield
        done = True
        print(currentTargets[0], targetPositions[0])
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
    # TODO
    stuff = 0