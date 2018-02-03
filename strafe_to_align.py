import wpilib
import ctre
import seamonsters as sea
import math
from networktables import NetworkTables

def strafeAlign(drive,vision,visionOffset):

    while True:
        yield
        sea.sendLogStates()

        hasTarget = vision.getNumber('tv', "no visionX")
        xOffset = vision.getNumber('tx', "no visionX")
        exponent = 0.8
        if xOffset == "no visionX" or not hasTarget:
            print('no vision')
            continue
        totalOffset = xOffset - visionOffset
        exOffset = abs(totalOffset) ** exponent / 13.9
        if abs(totalOffset) <= 0.5:
            #Original tolerance: 1
            print('done')
            continue
        elif totalOffset < -0.5:
            drive.drive(-exOffset,0,0)
            print(xOffset)
        elif totalOffset > 0.5:
            drive.drive(exOffset,0,0)
            print(xOffset)









