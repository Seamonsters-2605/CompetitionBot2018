import math
import auto_driving
import auto_vision
import seamonsters as sea
import auto_navx
import wpilib

# Names: start location, switch direction, strategy

def loc1_left_switchFront(drive, rotationTracker):
    print("running loc1_left_switchFront")
    yield from auto_driving.driveDistance(drive, 15, .33)
    rotationTracker.setTargetOffsetRotation(45)
    yield from auto_driving.driveDistance(drive, 42, .33)
    rotationTracker.setTargetOffsetRotation(0)
    '''for i in range(75):
        drive.drive(.3, 0, 0)
        yield'''
    yield
    drive.drive(0, 0, 0)

def loc1_right_switchFront(drive, rotationTracker):
    print("running loc1_right_switchFront")
    yield from auto_driving.driveDistance(drive, 40, .33)
    rotationTracker.setTargetOffsetRotation(90)
    yield from auto_driving.driveDistance(drive, 122, .33)
    rotationTracker.setTargetOffsetRotation(0)
    #yield from auto_driving.driveDistance(drive,70,.33)
    yield
    drive.drive(0,0,0)

def loc1_crossLine(drive, rotationTracker):
    print("running loc1_crossLine")
    yield from auto_driving.driveDistance(drive, 120, .33)

def loc2_left_switchFront(drive, rotationTracker):
    print("running loc2_left_switchFront")
    yield from auto_driving.driveDistance(drive, 35, .33)
    rotationTracker.setTargetOffsetRotation(-90)
    #yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive,100,.33)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0, 0, 0)

def loc2_right_switchFront(drive, rotationTracker):
    print("running loc2_right_switchFront")
    yield from auto_driving.driveDistance(drive, 12, .33)
    rotationTracker.setTargetOffsetRotation(45)
    yield from auto_driving.driveDistance(drive, 57, .33)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0, 0, 0)

def loc2_left_crossLine(drive, rotationTracker):
    print("running loc2_left_crossLine")
    rotationTracker.setTargetOffsetRotation(90)
    yield from auto_driving.driveDistance(drive, 45, .33)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0, 0, 0)

def loc2_right_crossLine(drive, rotationTracker):
    print("running loc2_right_crossLine")
    rotationTracker.setTargetOffsetRotation(-90)
    yield from auto_driving.driveDistance(drive,100,.33)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0, 0, 0)

def loc3_left_switchFront(drive, rotationTracker):
    print("running loc3_left_switchFront")
    yield from auto_driving.driveDistance(drive, 35, .33)
    rotationTracker.setTargetOffsetRotation(-90)
    yield from auto_driving.driveDistance(drive, 200, .45)
    rotationTracker.setTargetOffsetRotation(0)

def loc3_right_switchFront(drive, rotationTracker):
    print("running loc3_right_switchFront")
    yield from auto_driving.driveDistance(drive, 15, .33)
    rotationTracker.setTargetOffsetRotation(-45)
    yield from auto_driving.driveDistance(drive, 57, .33)
    rotationTracker.setTargetOffsetRotation(0)
    yield
    drive.drive(0, 0, 0)

def loc3_crossLine(drive, rotationTracker):
    print("running loc3_crossLine")
    yield from auto_driving.driveDistance(drive, 120, .33)

