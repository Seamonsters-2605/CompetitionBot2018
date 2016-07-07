__author__ = "jacobvanthoog"

import wpilib
import sys
import builtins
from seamonsters.wpilib_sim.simUtils import *

def run(robotClass):
    try:
        builtins.blenderWpilibEnabled
    except AttributeError:
        print("No blender sim")
    else:
        print("Blender simulation for robot:", robotClass)
        def updateBlenderTalons():
            blenderTalons = builtins.blenderWpilibTalons
            for t in getCANTalons():
                port = t.port
                if port < len(blenderTalons):
                    blenderTalon = blenderTalons[t.port]
                    if blenderTalon != None:
                        blenderTalon.setTorque(t.getOutputVoltage() / 12.0)
        
        print("Create robot")
        robot = robotClass()
    
        print("Robot init")
        robot.robotInit()

        print("Teleop init")
        robot.teleopInit()

        addUpdateFunction(updateBlenderTalons)
        
        def blenderLoop():
            robot.teleopPeriodic()
            for f in getUpdateFunctions():
                f()
        builtins.blenderWpilibLoop = blenderLoop

        return

    
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


try:
    builtins.blenderWpilibEnabled
except AttributeError:
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'wpilib_sim':
            print("Simulate!")
            replaceWpilib()
            wpilib.run = run
else:
    print("Blender sim!")
    replaceWpilib()
    wpilib.run = run
