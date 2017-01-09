__author__ = "jacobvanthoog"

import wpilib
import wpilib.command

class Module( wpilib.IterativeRobot ):
    """
    An IterativeRobot that is able to contain other robots. If you subclass this
    and override __init__ or special robot functions like robotInit or
    teleopPeriodic, make sure you call super()'s versions of those functions.
    """
    
    def __init__(self, initSuper=True):
        if initSuper:
            super().__init__()
        self.Modules = [ ]
        self.Parent = None
        self.Time = 0

    def parent(self):
        """
        Get the Module that owns this Module
        """
        return self.Parent
    
    def setParent(self, parent):
        """
        Internal function to set the parent Module of this Module
        """
        self.Parent = parent
    
    def time(self):
        """
        Get the number of iterations since the start of the disabled,
        autonomous, teleop, or test loop.
        """
        return self.Time

    def addModule(self, robot):
        """
        Add a sub-robot to use in the robot. When special robot functions like
        robotInit or teleopPeriodic are called, they will also be called for
        each sub-robot. If the robot happens to be a Module, its parent will be
        set.
        """
        self.Modules.append(robot)
        if isinstance(robot, Module):
            robot.setParent(self)
    
    def getModule(self, moduleType):
        """
        Find a sub-Module given its class.
        """
        for robot in self.Modules:
            if type(robot) == moduleType:
                return robot
        return None
    
    def runModules(self, function):
        """
        Internal function to apply a given function to each module
        """
        for robot in self.Modules:
            try:
                function(robot)
            except BaseException as e:
                print("Error in module", type(robot).__name__, ":", str(e))
    
    def robotInit(self):
        self.Time = 0
        def f(r):
            r.robotInit()
        self.runModules(f)

    def disabledInit(self):
        wpilib.command.Scheduler.getInstance().run()
        self.Time = 0
        def f(r):
            r.disabledInit()
        self.runModules(f)

    def autonomousInit(self):
        wpilib.command.Scheduler.getInstance().run()
        self.Time = 0
        def f(r):
            r.autonomousInit()
        self.runModules(f)

    def teleopInit(self):
        wpilib.command.Scheduler.getInstance().run()
        self.Time = 0
        def f(r):
            r.teleopInit()
        self.runModules(f)

    def testInit(self):
        wpilib.command.Scheduler.getInstance().run()
        self.Time = 0
        def f(r):
            r.testInit()
        self.runModules(f)

    def disabledPeriodic(self):
        wpilib.command.Scheduler.getInstance().run()
        def f(r):
            r.disabledPeriodic()
        self.runModules(f)
        self.Time += 1

    def autonomousPeriodic(self):
        wpilib.command.Scheduler.getInstance().run()
        def f(r):
            r.autonomousPeriodic()
        self.runModules(f)
        self.Time += 1

    def teleopPeriodic(self):
        wpilib.command.Scheduler.getInstance().run()
        def f(r):
            r.teleopPeriodic()
        self.runModules(f)
        self.Time += 1

    def testPeriodic(self):
        wpilib.command.Scheduler.getInstance().run()
        def f(r):
            r.testPeriodic()
        self.runModules(f)
        self.Time += 1
