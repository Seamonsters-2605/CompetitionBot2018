__author__ = "jacobvanthoog"

from seamonsters.utilityBots.encoderTest import EncoderTest
import wpilib

class Test(EncoderTest):
    def __init__(self):
        EncoderTest.__init__(self, [0, 1, 2, 3])
        
if __name__ == "__main__":
    wpilib.run(Test)