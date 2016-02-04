__author__ = "jacobvanthoog"

import wpilib
import random, sys


class PDPLogger:
    def __init__(self, pdp):
        self.PDP = pdp

    def getAllCurrents(self):
        currents = [self.PDP.getCurrent(i) for i in range(0,16)]
        
        return currents

    def printCurrents(self):
        for i in range(0, 8):
            message = self.currentMessage(i) + "    "
            message += self.currentMessage(i+8)
            print(message)

    def reprintCurrents(self):
        #up 8 lines
        for i in range(0, 8):
            sys.stdout.write("\033[F")
        self.printCurrents();

    def currentMessage(self, channel):
        current = self.getAllCurrents()[channel]
        message = '%02d' % channel + ": " + ("{:8.4f}".format(current))
        return message

