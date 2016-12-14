__author__ = "jacobvanthoog"

import wpilib
from seamonsters.logging import LogState

class PDPMonitor:
    """
    Monitors and prints the current of a group of PDP channels.
    """
    def __init__(self, channels):
        """
        ``channels`` is a list of channel numbers (0 - 15) to monitor.
        """
        self.channels = channels
        self.pdp = wpilib.PowerDistributionPanel()
        # updates every 0.8 seconds
        self.logStates = [LogState("PDP " + str(c), 0.8) for c in channels]
    
    def update(self):
        """
        Call this every loop (50 times per second) to monitor the currents.
        """
        for i in range(0, len(self.channels)):
            self.logStates[i].update(self.pdp.getCurrent(self.channels[i]))

