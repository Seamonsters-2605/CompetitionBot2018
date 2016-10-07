__author__ = "jacobvanthoog"

from seamonsters.wpilib_sim import simulate
import wpilib
from seamonsters.modularRobot import Module
from stingray.drive import StingrayDrive
from stingray.shooter import StingrayShooter

class StingrayBot(Module):
    
    def __init__(self):
        super().__init__()
        self.addModule(StingrayDrive())
        self.addModule(StingrayShooter())
        
if __name__ == "__main__":
    wpilib.run(StingrayBot)
