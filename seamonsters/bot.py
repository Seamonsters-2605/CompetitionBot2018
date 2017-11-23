__author__ = "seamonsters"

import hal
import seamonsters

from wpilib.robotbase import RobotBase
from wpilib.livewindow import LiveWindow

class CommandBot(RobotBase, seamonsters.CommandGroup):

    def __init__(self):
        RobotBase.__init__(self)
        seamonsters.CommandGroup.__init__(self)
        self.started = False

    def __repr__(self):
        return "Robot"

    def startCompetition(self):
        hal.report(hal.UsageReporting.kResourceType_Framework,
                   hal.UsageReporting.kFramework_Iterative)

        self.robotInit()

        # Tell the DS that the robot is ready to be enabled
        hal.observeUserProgramStarting()

        # loop forever, calling the appropriate mode-dependent function
        LiveWindow.setEnabled(False)
        while True:
            # Wait for new data to arrive
            self.ds.waitForData()
            # Call the appropriate function depending upon the current robot mode
            if self.isDisabled():
                if self.state != seamonsters.Command.STOPPED:
                    self.interrupt()
                    self.run()
                    LiveWindow.setEnabled(False)
                hal.observeUserProgramDisabled()
                self.started = False
            else: # not disabled
                if not self.started:
                    LiveWindow.setEnabled(True)
                    self.started = True
                    self.start()
                    self.clear()

                if self.isTest():
                    hal.observeUserProgramTest()
                elif self.isAutonomous():
                    hal.observeUserProgramAutonomous()
                else:
                    hal.observeUserProgramTeleop()

                self.run()

    def robotInit(self):
        """
        Override this for robot initialization.
        """
        print("No robotInit!")
