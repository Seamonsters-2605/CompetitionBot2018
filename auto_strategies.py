import math
import auto_driving
import auto_vision
import seamonsters as sea
import auto_navx
import wpilib

def left_left(drive, angleHolder):
    print("running left_left")
    yield from auto_driving.driveDistance(drive, 15, .33)
    angleHolder[0] = 45
    yield from auto_driving.driveDistance(drive, 45, .33)
    angleHolder[0] = 0
    #yield from auto_driving.driveDistance()
    '''for i in range(75):
        drive.drive(.3, 0, 0)
        yield'''
    drive.drive(0, 0, 0)

def left_right(drive, angleHolder):
    print("running left_right")
    yield from auto_driving.driveDistance(drive, 25, .33)
    angleHolder[0] = 90
    yield from auto_driving.driveDistance(drive, 115, .33)
    angleHolder[0] = 0
    #yield from auto_driving.driveDistance(drive,70,.33)
    yield
    drive.drive(0,0,0)

def left_cross(drive, angleHolder):
    print("running left_cross")
    yield from auto_driving.driveDistance(drive, 120, .33)

def mid_left(drive, angleHolder):
    print("running mid_left")
    yield from auto_driving.driveDistance(drive, 33, .33)
    angleHolder[0] = -90
    #yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive,85,.33)
    angleHolder[0] = 0
    yield
    drive.drive(0, 0, 0)
    '''for i in range(90):
        drive.drive(-i / 150, 0, 0)
        yield'''

def mid_right(drive, angleHolder):
    print("running mid_right")
    yield from auto_driving.driveDistance(drive, 50, .33)
    angleHolder[0] = 90
    yield from auto_driving.driveDistance(drive,4,.33)
    angleHolder[0] = 0
    yield
    drive.drive(0, 0, 0)

def mid_cross_right(drive, angleHolder):
    print("running mid_cross_right")
    angleHolder[0] = 90
    yield from auto_driving.driveDistance(drive, 30, .33)
    angleHolder[0] = 0
    yield
    drive.drive(0, 0, 0)

def mid_cross_left(drive, angleHolder):
    print("running mid_cross_left")
    angleHolder[0] = -90
    yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive,100,.33)
    angleHolder[0] = 0
    yield
    drive.drive(0, 0, 0)

def right_left(drive, angleHolder):
    print("running right_left")
    yield from auto_driving.driveDistance(drive, 40, .33)
    angleHolder[0] = -90
    yield from auto_driving.driveDistance(drive, 200, .33)
    angleHolder[0] = 0

def right_right(drive, angleHolder):
    print("running right_right")
    yield from auto_driving.driveDistance(drive, 57, .33)
    angleHolder[0] = -90
    yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive,45,.33)
    angleHolder[0] = 0
    drive.drive(0, 0, 0)

def right_cross(drive, angleHolder):
    print("running right_cross")
    yield from auto_driving.driveDistance(drive, 120, .33)

