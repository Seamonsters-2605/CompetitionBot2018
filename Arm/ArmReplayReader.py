__author__ = "jacobvanthoog"

class ArmReplayReader:

    def __init__(self, replay, filePath):
        self.Arm = replay
        file = open(filePath)
        lines = file.readlines()
        self.Positions = [None for i in range(0, len(lines))]
        i = 0
        for line in lines:
            numberStrs = line.split(' ', 1)
            position = ( float(numberStrs[0]), float(numberStrs[1]) )
            self.Positions[i] = position
            i += 1
        print(self.Positions)
        self.resetPath()
        self.disable()

    def resetPath(self):
        self.Point = 0 # index in self.Positions
        self.Started = False

    def enable(self):
        self.Enabled = True

    def disable(self):
        self.Disabled = False

    def update(self):
        if not self.Enabled:
            return
        
        if not self.Started:
            self.Arm.setTarget(self.Positions[self.Point])
            return

        if self.Arm.movementCompleted():
            print("Point", self.Point, "reached!")
            self.Point += 1
            if self.Point == len(self.Positions):
                self.disable()
                self.resetPath()
                return
            self.Arm.setTarget(self.Positions[self.Point])

        return

