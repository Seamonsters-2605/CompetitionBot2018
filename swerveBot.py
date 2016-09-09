__author__ = "jacobvanthoog"

import wpilib
from seamonsters.modularRobot import Module
from swerveBot.swerveBotDrive import SwerveBotDrive

class SwerveBot(Module):
    
    def __init__(self):
        super().__init__()
        self.addModule(SwerveBotDrive())
        
if __name__ == "__main__":
    wpilib.run(SwerveBot)