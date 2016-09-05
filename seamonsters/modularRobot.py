__author__ = "jacobvanthoog"

import wpilib

# An IterativeRobot that is able to contain other robots
class Module( wpilib.IterativeRobot ):
    
    def __init__(self):
        self.Modules = [ ]
        self.Parent = None
        self.Time = 0

    # Get the Module that owns this Module
    def parent(self):
        return self.Parent
    
    # internal function
    def setParent(self, parent):
        self.Parent = parent
    
    # Get the number of iterations since the start of the disabled, autonomous,
    # teleop, or test loop.
    def time(self):
        return self.Time

    # Add a sub-Module to use in the robot
    def addModule(self, module):
        self.Modules.append(module)
        module.setParent(self)

    # Get a previously added Module
    # moduleType is the class of the Module
    def getModule(self, moduleType):
        for robot in self.Modules:
            if type(robot) == moduleType:
                return robot
        return None

    # internal function to apply a function to all modules
    def runModules(self, function):
        for robot in self.Modules:
            try:
                function(robot)
            except BaseException as e:
                print("Error in module", type(robot).__name__, ":", str(e))
                
    # IterativeRobot functions
    # If you implement your own, make sure to call super()'s version also.
    
    def robotInit(self):
        self.Time = 0
        def f(r):
            r.robotInit()
        self.runModules(f)

    def disabledInit(self):
        self.Time = 0
        def f(r):
            r.disabledInit()
        self.runModules(f)

    def autonomousInit(self):
        self.Time = 0
        def f(r):
            r.autonomousInit()
        self.runModules(f)

    def teleopInit(self):
        self.Time = 0
        def f(r):
            r.teleopInit()
        self.runModules(f)

    def testInit(self):
        self.Time = 0
        def f(r):
            r.testInit()
        self.runModules(f)

    def disabledPeriodic(self):
        def f(r):
            r.disabledPeriodic()
        self.runModules(f)
        self.Time += 1

    def autonomousPeriodic(self):
        def f(r):
            r.autonomousPeriodic()
        self.runModules(f)
        self.Time += 1

    def teleopPeriodic(self):
        def f(r):
            r.teleopPeriodic()
        self.runModules(f)
        self.Time += 1

    def testPeriodic(self):
        def f(r):
            r.testPeriodic()
        self.runModules(f)
        self.Time += 1
