import wpilib
import ctre
import seamonsters as sea
import math
from networktables import NetworkTables

def strafeAlign(drive,vision,visionOffset):

    while True:
        yield
        sea.sendLogStates()
        xOffset = vision.getNumber('tx',"no visionX")
        exponent = 0.8
        if xOffset == "no visionX":
            print('no vision')
            continue
        totalOffest = xOffset - visionOffset
        exOffset = abs(totalOffest) ** exponent / 13.9
        if totalOffest < 0:
            drive.drive(-exOffset,0,0)
        if totalOffest > 0:
            drive.drive(exOffset,0,0)
        if abs(totalOffest) <= 0.5:
            #Original tolerance: 1
            continue
        # Original: exponent:0.65, denominator:15









