import wpilib
import seamonsters as sea
import drive
import shooter
import time

class MainRobot(sea.GeneratorBot):

    def robotInit(self):
        self.driverJoystick = wpilib.Joystick(0)

        self.driveBot = drive.DriveBot.__new__(drive.DriveBot)
        self.driveBot.theRobot = self
        self.driveBot.driverJoystick = self.driverJoystick
        drive.DriveBot.robotInit(self.driveBot)

        self.shooterInstance = sea.IterativeRobotInstance(shooter.MyRobot)
        self.shooterBot = self.shooterInstance.robotObject
        self.shooterBot.theRobot = self
        self.shooterBot.driverJoystick = self.driverJoystick

        self.timerLogState = sea.LogState("Time")

    def timer(self):
        last_t = time.time()
        timeDiff = 0
        i = 0
        while True:
            i += 1
            if i % 50 == 0:
                new_t = time.time()
                timeDiff = new_t - last_t
                last_t = new_t
            self.timerLogState.update('%.3f' % timeDiff)
            yield

    def test(self):
        yield from sea.parallel(drive.DriveBot.test(self.driveBot),
                                self.timer(),
                                self.sendLogStatesGenerator())

    def sendLogStatesGenerator(self):
        while True:
            yield
            sea.sendLogStates()

    def teleop(self):
        yield from sea.parallel(
            drive.DriveBot.teleop(self.driveBot),
            self.shooterInstance.teleopGenerator(),
            self.timer(),
            self.sendLogStatesGenerator())

    def autonomous(self):
        yield from sea.parallel(drive.DriveBot.autonomous(self.driveBot),
                                self.timer(),
                                self.sendLogStatesGenerator())

if __name__ == "__main__":
    wpilib.run(MainRobot)
