__author__ = "seamonsters"

import traceback
import hal
from wpilib.robotbase import RobotBase
from wpilib.livewindow import LiveWindow

class GeneratorBot(RobotBase):

    def __init__(self):
        RobotBase.__init__(self)
        self.iterator = None
        self.earlyStop = False

    def startCompetition(self):
        hal.report(hal.UsageReporting.kResourceType_Framework,
                   hal.UsageReporting.kFramework_Iterative)

        self.robotInit()

        # Tell the DS that the robot is ready to be enabled
        hal.observeUserProgramStarting()

        LiveWindow.setEnabled(False)
        while True:
            # Wait for new data to arrive
            self.ds.waitForData()
            if self.isDisabled():
                self.earlyStop = False
                if self.iterator:
                    self.iterator.close()
                    self.iterator = None
                    LiveWindow.setEnabled(False)
                hal.observeUserProgramDisabled()
            else: # not disabled
                if not self.iterator and not self.earlyStop:
                    LiveWindow.setEnabled(True)
                    try:
                        if self.isTest():
                            self.iterator = self.test()
                        elif self.isAutonomous():
                            self.iterator = self.autonomous()
                        else:
                            self.iterator = self.teleop()
                    except:
                        print("Exception while starting sequence!")
                        traceback.print_exc()
                        self.earlyStop = True

                if self.isTest():
                    hal.observeUserProgramTest()
                elif self.isAutonomous():
                    hal.observeUserProgramAutonomous()
                else:
                    hal.observeUserProgramTeleop()

                if self.iterator:
                    try:
                        next(self.iterator)
                    except StopIteration:
                        print("Robot done.")
                        self.iterator = None
                        self.earlyStop = True
                    except:
                        print("Exception in robot code!")
                        traceback.print_exc()
                        self.iterator = None
                        self.earlyStop = True

    def robotInit(self):
        """
        Override this for robot initialization. This should NOT be a generator.
        """
        print("No robotInit!")

    def teleop(self):
        """
        Override this to make a generator for teleop
        """
        print("No teleop!")
        yield

    def autonomous(self):
        """
        Override this to make a generator for autonomous
        """
        print("No autonomous!")
        yield

    def test(self):
        """
        Override this to make a generator for test mode
        """
        print("No test!")
        yield
