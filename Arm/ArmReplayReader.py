__author__ = "jacobvanthoog"

class ArmReplayReader:

    def __init__(self, filePath):
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

arm = ArmReplayReader("/Users/Jacob van't Hoog/testPath.txt")
