__author__ = "jacobvanthoog"
from wpilib.command import Scheduler, Command, CommandGroup, PrintCommand
from xml.etree import ElementTree # XML

PIXELS_PER_INCH = 16


class ArmPath:

    def __init__(self, filePath):
        self.FilePath = filePath
        print('Load arm path: ' + str(filePath) + '...')
        tree = ElementTree.parse(filePath)
        root = tree.getroot()
        path = root.find('{http://www.w3.org/2000/svg}path')
        pathData = str(path.get('d'))

        pathData = pathData.split('C', maxsplit=1)[1] # get all text after "C"
        pathData = pathData.strip()
        pathLines = pathData.split()

        numPoints = int(len(pathLines) / 3) + 1
        print('Path has', numPoints, 'points.')

        points = [ None for i in range(0, numPoints) ]
        points[0] = self.parseLine(pathLines[0])
        for i in range(1, numPoints):
            line = pathLines[i * 3 - 2]
            points[i] = self.parseLine(line)

        viewBox = root.get('viewBox')
        imageHeight = int(viewBox.split()[3])

        self.PathPoints = [self.imageCoordinatesToInches(p, imageHeight)
                           for p in points]

        print(self.PathPoints)

    def getPoints(self):
        return self.PathPoints

    def getFollowCommand(self, armControl):
        commandGroup = CommandGroup()
        commandGroup.addSequential(
            PrintCommand('Following path ' + self.FilePath + '...'))

        for point in self.PathPoints:
            command = ArmCommand(armControl, point)
            commandGroup.addSequential(command)

        commandGroup.addSequential(PrintCommand('Path complete!'))

        return commandGroup


    # DON'T USE THESE FUNCTIONS

    def parseLine(self, line):
        values = line.strip().split(',', 1)
        return (float(values[0]), float(values[1]))

    def imageCoordinatesToInches(self, coords, imageHeight):
        x = coords[0] / float(PIXELS_PER_INCH) - 1
        y = (imageHeight - coords[1]) / float(PIXELS_PER_INCH) - 1
        return (x, y)
        return (x, y)


class ArmCommand(Command):

    def __init__(self, arm, point):
        super().__init__()
        self.Arm = arm
        self.Point = point
        self.Started = False

    def initialize(self):
        self.Arm.moveToPosition(self.Point[0], self.Point[1])
        self.Started = True

    def execute(self): # called in a loop
        pass

    def interrupted(self):
        self.end()

    def end(self):
        pass

    def isFinished(self):
        if not self.Started:
            return False
        return self.Arm.movementCompleted()
