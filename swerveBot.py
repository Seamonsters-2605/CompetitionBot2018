__author__ = "jacobvanthoog"

from seamonsters.wpilib_sim import simulate
import wpilib
from seamonsters.modularRobot import Module
from swerveBot.swerveBotDrive import SwerveBotDrive
from swerveBot.swerveBotShooter import SwerveBotShooter

class SwerveBot(Module):
    
    def __init__(self, normalScale=.35, fastScale=.5, slowScale=.2):
        super().__init__()
        self.addModule(SwerveBotDrive())
        self.addModule(SwerveBotShooter())
        
if __name__ == "__main__":
    wpilib.run(SwerveBot)
