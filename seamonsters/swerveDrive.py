__author__ = "jacobvanthoog"

from drive import DriveInterface
import math

def magnitude(vector):
    return math.sqrt(vector[0]**2.0 + vector[1]**2.0)

def direction(vector):
    return math.atan2(vector[1], vector[0])

def normalize(vector):
    mag = magnitude(vector)
    return (vector[0] / mag, vector[1] / mag)

class WheelState:
    # location is a tuple (x, y) -- location of wheel from center of robot
    def __init__(self, location, driveTalon, rotateTalon):
        self.location = location
        self.driveVector = (0, 0)
        self.targetDirection = 0
        self.targetMagnitude = 0
        self.driveTalon = driveTalon
        self.rotateTalon = rotateTalon
    
    def calcDrive(self, mag, driveDirection, turn):
        moveVector = (math.cos(driveDirection) * mag,
                math.sin(driveDirection) * mag)
        self.driveVector = (moveVector[0] - self.location[1]*turn,
                moveVector[1] + self.location[0]*turn)
        self.targetMagnitude = magnitude(self.driveVector)
        self.targetDirection = direction(self.driveVector)

class SwerveDrive(DriveInterface):
    
    def __init__(self):
        DriveInterface.__init__(self)
        self.wheels = [ ]
    
    def addWheel(self, location):
        self.wheels.append(WheelState(location))
    
    def drive(self, magnitude, direction, turn, forceDriveMode = None):
        for wheel in self.wheels:
            wheel.calcDrive(magnitude, direction, turn)
    
    def printWheelState(self):
        for i, wheel in enumerate(self.wheels):
            print("Wheel:", i,
                  "Vector:", wheel.driveVector,
                  "Magnitude:", wheel.targetMagnitude,
                  "Direction:", math.degrees(wheel.targetDirection))


drive = SwerveDrive()
drive.addWheel((1.0,1.0))
drive.addWheel((-1.0,1.0))
drive.addWheel((1.0,-1.0))
drive.addWheel((-1.0,-1.0))
drive.drive(5, math.radians(90), 4)
drive.printWheelState()