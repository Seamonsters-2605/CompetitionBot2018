"""
3 numbers on each line, separated by spaces:
    Frame, X, Y

Starting on the starting line, positive Y is forward and positive X is right.
"""

import math
import seamonsters as sea
import auto_driving
import robotconfig

def readPoints(filename):
    points = [ ]
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            values = line.split(' ')
            try:
                values = tuple((float(v) for v in values))
            except ValueError:
                print("Couldn't read line", line)
                continue
            points.append(values)
    return points
def switchingSwerveMotor(self, Fr, Br, Fl, Bl):#need motor names to switch using these as place holders
    if swerveDr = True:
        if guideAngle > (math.pi/2)  and angle < math.pi #first quadrent 
        
        if guideAngle >= math.pi and angle < 3*(math.pi/2):
         
        if guideAngle >= 3*(math.pi/2) anf guideAngle < 2*math.pi:
            
        if guideAngle >=


def scriptedAutoSequence(filename, drive, rotationTracker):
    try:
        points = readPoints(filename)
    except FileNotFoundError:
        print("File not found: " + filename + "!")
        return
    if len(points) <= 1:
        print("Not enough points!")
        return
    point0 = points[0]
    for point1 in points[1:]:
        print("Moving from", point0, "to", point1)
        xOffset = (point1[1] - point0[1]) * 12
        yOffset = (point1[2] - point0[2]) * 12
        distance = math.sqrt(xOffset ** 2 + yOffset ** 2)
        timeDiff = point1[0] - point0[0]
        if distance > 1e-6 and timeDiff > 0:
            # radians, positive counter-clockwise, 0 is right
            angle = math.atan2(yOffset, xOffset)
            # degrees, positive clockwise, 0 is forward
            angle = -math.degrees(angle) + 90
            currentAngle = rotationTracker.targetOffsetRotation
            while angle - currentAngle > 180:
                angle -= 360
            while currentAngle - angle > 180:
                angle += 360
            distance_ticks = distance / robotconfig.wheelCircumference \
                             * robotconfig.ticksPerWheelRotation
            speed = distance_ticks / timeDiff / robotconfig.maxVelocityPositionMode
            print("Distance", distance, "Angle", angle, "Speed", speed)
            rotationTracker.setTargetOffsetRotation(angle)
            yield from auto_driving.driveDistance(drive, distance, speed,
                                                  dualMotor=True)
        else:
            yield from sea.wait(int(timeDiff))

        point0 = point1
