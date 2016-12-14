__author__ = "jacobvanthoog"

import wpilib
from seamonsters.logging import LogState

class PDPMonitor:

    def __init__(self, channels):
        """
        ``channels`` is a list of channel numbers (0 - 15)
        """
        self.channels = channels
        self.pdp = wpilib.PowerDistributionPanel()
        # updates every 0.8 seconds
        self.logStates = [LogState("PDP " + str(c), 0.8) for c in channels]
    
    def update(self):
        for i in range(0, len(self.channels)):
            self.logStates[i].update(self.pdp.getCurrent(self.channels[i]))

