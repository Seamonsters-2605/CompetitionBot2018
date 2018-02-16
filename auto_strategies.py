import math
import auto_driving
import auto_vision
import seamonsters as sea
import auto_navx
import wpilib

def left_left(drive, angleHolder):
    print("running left_left")
    yield from auto_driving.driveDistance(drive, 50, .3)
    yield
    drive.drive(0, 0, 0)
    for i in range(75):
        drive.drive(.3, 0, 0)
        yield
    drive.drive(0, 0, 0)

def left_right(drive, angleHolder):
    print("running left_right")
    yield from auto_driving.driveDistance(drive, 25, .3)
    angleHolder[0] = 90
    yield from auto_driving.driveDistance(drive, 125, .3)
    angleHolder[0] = 0
    yield from auto_driving.driveDistance(drive,60,.3)
    print("addition run")
    yield
    drive.drive(0,0,0)

def left_cross(drive, angleHolder):
    print("running left_cross")
    yield from auto_driving.driveDistance(drive, 120, .3)

def mid_left(drive, angleHolder):
    print("running mid_left")
    yield from auto_driving.driveDistance(drive, 50, .3)
    yield
    drive.drive(0, 0, 0)
    for i in range(90):
        drive.drive(-i / 150, 0, 0)
        yield

def mid_right(drive, angleHolder):
    print("running mid_right")
    yield from auto_driving.driveDistance(drive, 50, .3)
    angleHolder[0] = 90
    yield from auto_driving.driveDistance(drive,4,.3)
    angleHolder[0] = 0
    yield
    drive.drive(0, 0, 0)
    '''for i in range(65):
        drive.drive(i / 120, 0, 0)
        yield'''
def mid_cross_right(drive, angleHolder):
    print("running mid_cross_right")
    angleHolder[0] = 90
    yield from auto_driving.driveDistance(drive, 40, .3)
    '''for i in range(150):
        drive.drive(i / 300, 0, 0)'''
    angleHolder[0] = 0
    yield
    drive.drive(0, 0, 0)

def mid_cross_left(drive, angleHolder):
    print("running mid_cross_left")
    angleHolder[0] = -90
    yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive,100,.3)
    angleHolder[0] = 0
    yield
    drive.drive(0, 0, 0)

def right_left(drive, angleHolder):
    print("running right_left")
    yield from auto_driving.driveDistance(drive, 40, .3)
    angleHolder[0] = -90
    yield from auto_driving.driveDistance(drive, 200, .3)
    angleHolder[0] = 0

def right_right(drive, angleHolder):
    print("running right_right")
    yield from auto_driving.driveDistance(drive, 55, .3)
    angleHolder[0] = -90
    yield from sea.wait(30)
    yield from auto_driving.driveDistance(drive,45,.3)
    angleHolder[0] = 0
    drive.drive(0, 0, 0)
    '''for i in range(65):
        drive.drive(-.3, 0, 0)
        yield
    drive.drive(0, 0, 0)'''

def right_cross(drive, angleHolder):
    print("running right_cross")
    yield from auto_driving.driveDistance(drive, 120, .3)

