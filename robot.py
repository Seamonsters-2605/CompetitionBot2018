import wpilib
import seamonsters as sea
import drive
import shooter
import time

class MainRobot(sea.GeneratorBot):

    def robotInit(self):
        self.driverJoystick = wpilib.Joystick(0)
        self.driveObject = drive.DriveBot.__new__(drive.DriveBot)
        self.driveObject.driverJoystick = self.driverJoystick
        self.driveObject.theRobot = self
        drive.DriveBot.robotInit(self.driveObject)
        self.shooterInstance = sea.IterativeRobotInstance(shooter.MyRobot)

        self.shooterInstance.robotObject.joystick = self.driverJoystick
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
        yield from sea.parallel(drive.DriveBot.test(self.driveObject),
                                self.timer(),
                                self.sendLogStatesGenerator())

    def sendLogStatesGenerator(self):
        while True:
            yield
            sea.sendLogStates()

    def teleop(self):
        yield from sea.parallel(
            drive.DriveBot.teleop(self.driveObject),
            self.shooterInstance.teleopGenerator(),
            self.timer(),
            self.sendLogStatesGenerator())

    def autonomous(self):
        yield from sea.parallel(drive.DriveBot.autonomous(self.driveObject),
                                self.timer(),
                                self.sendLogStatesGenerator())

if __name__ == "__main__":
    wpilib.run(MainRobot)
