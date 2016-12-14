__author__ = "jacobvanthoog"

import wpilib
from seamonsters.logging import LogState

class EncoderTest(wpilib.IterativeRobot):
    
    def __init__(self, ports):
        """
        ports is an array of integers for the CANTalon ports to test
        """
        super().__init__()
        self.talons = [wpilib.CANTalon(p) for p in ports]
        self.logStates = [LogState("Talon " + str(p)) for p in ports]
        for t in self.talons:
            t.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)

    def teleopPeriodic(self):
        for i in range(0, len(self.talons)):
            self.logStates[i].update(self.talons[i].getPosition())

