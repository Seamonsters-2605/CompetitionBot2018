import math
import auto_driving
import auto_vision
import seamonsters as sea
import auto_navx
import wpilib

def left_left(drive, rotationTracker):
    print("running left_left")
    yield from auto_driving.driveDistance(drive, 15, .33)
    rotationTracker.setTargetOffsetRotation(45)
    yield from auto_driving.driveDistance(drive, 42, .33)
    rotationTracker.setTargetOffsetRotation(0)
    '''for i in range(75):
        drive.drive(.3, 0, 0)
        yield'''
    yield
    drive.drive(0, 0, 0)

def left_right(drive, rotationTracker):
    print("running left_right")
    yield from auto_driving.driveDistance(drive, 40, .33)
    rotationTracker.setTargetOffsetRotation(90)
    yield from auto_driving.driveDistance(drive, 122, .33)
    rotationTracker.setTargetOffsetRotation(0)
    #yield from auto_driving.driveDistance(drive,70,.33)
    yield
    drive.drive(0,0,0)

def left_cross(drive, rotationTracker):
    print("running left_cross")
    yield from auto_driving.driveDistance(drive, 120, .33)

def mid_left(drive, rotationTracker):
    print("running mid_left")
    yield from auto_driving.driveDistance(drive, 42, .33)
    rotationTracker.setTargetOffsetRotation(-90)
    #yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive,90,.33)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0, 0, 0)

def mid_right(drive, rotationTracker):
    print("running mid_right")
    yield from auto_driving.driveDistance(drive, 12, .33)
    rotationTracker.setTargetOffsetRotation(45)
    yield from auto_driving.driveDistance(drive, 57, .33)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0, 0, 0)

def mid_cross_right(drive, rotationTracker):
    print("running mid_cross_right")
    rotationTracker.setTargetOffsetRotation(90)
    yield from auto_driving.driveDistance(drive, 45, .33)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0, 0, 0)

def mid_cross_left(drive, rotationTracker):
    print("running mid_cross_left")
    rotationTracker.setTargetOffsetRotation(-90)
    yield from auto_driving.driveDistance(drive,100,.33)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0, 0, 0)

def right_left(drive, rotationTracker):
    print("running right_left")
    yield from auto_driving.driveDistance(drive, 40, .33)
    rotationTracker.setTargetOffsetRotation(-90)
    yield from auto_driving.driveDistance(drive, 200, .33)
    rotationTracker.setTargetOffsetRotation(0)

def right_right(drive, rotationTracker):
    print("running right_right")
    yield from auto_driving.driveDistance(drive, 15, .33)
    rotationTracker.setTargetOffsetRotation(-45)
    yield from auto_driving.driveDistance(drive, 57, .33)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0, 0, 0)

def right_cross(drive, rotationTracker):
    print("running right_cross")
    yield from auto_driving.driveDistance(drive, 120, .33)

