__author__ = "jacobvanthoog"

import wpilib
import sys


class PDPLogger:
    def __init__(self, pdp):
        self.PDP = pdp
        self.n = 0

    def getAllCurrents(self):
        currents = [self.PDP.getCurrent(i) for i in range(0,16)]

        #for testing without wpilib:
        #currents = [self.n for i in range(0, 16)]
        
        return currents

    def printCurrents(self):
        #will only display about once per second
        self.n = (self.n + 1)%50
        if not self.n == 1:
            return
        finalMessage = ""
        for i in range(0, 8):
            message = self.currentMessage(i) + "    "
            message += self.currentMessage(i+8)
            finalMessage += "\n" + message
        print(finalMessage)

    def reprintCurrents(self):
        # up 8 lines
        # this doesn't work on all terminals
        for i in range(0, 8):
            sys.stdout.write("\033[F")
        self.printCurrents();

    def currentMessage(self, channel):
        current = self.getAllCurrents()[channel]
        message = '%02d' % channel + ": " + ("{:8.4f}".format(current))
        return message
