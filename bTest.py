__author__ = "jacobvanthoog"

import seamonsters.wpilib_sim.simulate
import wpilib

class Test(wpilib.IterativeRobot):
    def robotInit(self):
        self.talon = wpilib.CANTalon(0)

    def teleopInit(self):
        self.talon.setControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        self.talon.set(1)

if __name__ == "__main__":
    wpilib.run(Test)
