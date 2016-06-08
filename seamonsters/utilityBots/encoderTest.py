__author__ = "jacobvanthoog"

import wpilib

class EncoderTest(wpilib.IterativeRobot):
    
    def __init__(self, ports):
        """
        ports is an array of integers for the CANTalon ports to test
        """
        wpilib.IterativeRobot.__init__(self)
        self.talons = [wpilib.CANTalon(p) for p in ports]
        for t in self.talons:
            t.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)

    def teleopPeriodic(self):
        for t in self.talons:
            print(t.getPosition(), end=" ")
        print("")