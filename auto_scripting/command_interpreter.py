"""
4 numbers on each line, separated by spaces:
    X, Y, Speed, Pause time
    Blender: X, Y, Z, Radius

Starting on the starting line, positive Y is forward and positive X is right.
"""

import math
import seamonsters as sea
import auto_driving

def readPoints(filename):
    points = [ ]
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            values = line.split(' ')
            if len(values) < 4:
                print("Couldn't read line", line)
                continue
            try:
                # get the first 4 numbers on each line
                values = tuple( (float(v) for v in values[:4]) )
            except ValueError:
                print("Coultn't read line", line)
                continue
            points.append(values)
    return points


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
        # pause
        if point0[3] > 0:
            yield from sea.wait(int(point0[3]) * 50)
        print("Moving from", point0, "to", point1)

        xOffset = point1[0] - point0[0]
        yOffset = point1[1] - point0[1]
        distance = math.sqrt(xOffset ** 2 + yOffset ** 2)
        # radians, positive counter-clockwise, 0 is right
        angle = math.atan2(yOffset, xOffset)
        # degrees, positive clockwise, 0 is forward
        angle = -math.degrees(angle) + 90

        rotationTracker.setTargetOffsetRotation(angle)
        yield from auto_driving.driveDistance(drive, distance, point0[2],
                                              dualMotor=True)

        point0 = point1

    # pause
    if point0[3] > 0:
        yield from sea.wait(int(point0[3]) * 50)
