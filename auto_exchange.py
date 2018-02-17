import auto_driving
import seamonsters as sea
import auto_navx
import wpilib
import auto_vision

def leftEx(drive, angleHolder):
    yield from auto_driving.driveDistance(drive, 60, .33)
    angleHolder[0] = 90
    yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive, 35, .33)
    angleHolder[0] = 180
    yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive, 30, .33)

def midEx(drive,angleHolder):
    yield from auto_driving.driveDistance(drive,40,.33)
    angleHolder[0] = -90
    yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive,50,.33)
    angleHolder[0] = -180
    yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive,25,.33)
    yield from auto_driving.driveDistance(drive,10,.33)