import wpilib
import ctre
import seamonsters as sea
import math
from networktables import NetworkTables

def strafeAlign(drive,vision):

    while True:
        yield
        sea.sendLogStates()
        xOffset = vision.getNumber('tx',"no visionX")
        exponent = 0.8
        exOffset = abs(xOffset)**exponent/13.9
        # Original: exponent:0.65, denominator:15
        #New1: exponent:0.67, denominator: 15
        #New2: exponent:0.67, denominator:13 ~not as gd as 15
        #New3: exponent:0.67, denominator: 14 ~ no noticable difference
        #New4: exponent:0.7, denominator: 13
        #New5: exponent:0.8, denom:13.9
        if xOffset == "no visionX":
            print('no vision')
            continue
        if xOffset < 0:
            drive.drive(-exOffset,0,0)
        if xOffset > 0:
            drive.drive(exOffset,0,0)
        if abs(xOffset) <= 0.5:
            #Original tolerance: 1
            #NewT1: 0.5
            continue








