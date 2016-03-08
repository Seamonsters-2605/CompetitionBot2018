__author__ = "jacobvanthoog"

PAUSE_STEPS = 25 # amount of time (in iterations) to pause before continuing


class ArmReplayReader:

    def __init__(self, replay, filePath):
        self.Arm = replay
        print("Reading file:", filePath)
        file = open("/home/lvuser/py/paths/" + filePath + ".txt")
        lines = file.readlines()
        self.Positions = [None for i in range(0, len(lines))]
        i = 0
        for line in lines:
            numberStrs = line.split(' ', 1)
            position = ( float(numberStrs[0]), float(numberStrs[1]) )
            self.Positions[i] = position
            i += 1
        print(self.Positions)
        self.Enabled = False
        self.Point = 0
        self.Started = False
        self.IsPaused = False # is pausing before setting the next point
        self.PauseTime = 0
        
    def enable(self):
        self.Enabled = True

    def disable(self):
        self.Enabled = False
        self.IsPaused = False
        self.PauseTime = False
        self.Point = 0 # index in self.Positions
        self.Started = False

    def update(self):
        if not self.Enabled:
            return
        
        if not self.Started:
            print("Starting...")
            self.Arm.setTarget(self.Positions[self.Point])
            self.Started = True
            return

        if self.IsPaused:
            self.PauseTime += 1
            if self.PauseTime >= PAUSE_STEPS:
                self.IsPaused = False
                self.Arm.setTarget(self.Positions[self.Point])
                print("Moving towards point", self.Point)
            return

        if self.Arm.movementCompleted():
            print("Point", self.Point, "reached!")
            self.Point += 1
            if self.Point == len(self.Positions):
                print("Path complete!")
                self.disable()
                return
            self.IsPaused = True
            self.PauseTime = 0

        return

