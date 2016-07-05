__author__ = "jacobvanthoog"

import wpilib
import sys
from seamonsters.wpilib_sim.simUtils import *

def run(robotClass):
    print("Simulating robot:", robotClass)
    
    print("Create robot")
    robot = robotClass()
    
    print("Robot init")
    robot.robotInit()
    
    if len(sys.argv) < 3:
        return
    
    command = sys.argv[2]
    if command == "d":
        print("Disabled init")
        robot.disabledInit()
        print("Disabled periodic")
        robotLoop(robot.disabledPeriodic)
        
    elif command == "a":
        print("Autonomous init")
        robot.autonomousInit()
        print("Autonomous periodic")
        robotLoop(robot.autonomousPeriodic)
        
    elif command == "t":
        print("Teleop init")
        robot.teleopInit()
        print("Teleop periodic")
        robotLoop(robot.teleopPeriodic)
        
    elif command == "s":
        print("Test init")
        robot.testInit()
        print("Test periodic")
        robotLoop(robot.testPeriodic)

if len(sys.argv) >= 2 and sys.argv[1] == 'wpilib_sim':
    print("Simulate!")
    replaceWpilib()
    wpilib.run = run
