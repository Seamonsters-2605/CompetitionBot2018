import wpilib
import seamonsters as sea
import drive
import shooter
import lifter
import time

class MainRobot(sea.GeneratorBot):

    def robotInit(self):
        self.driverJoystick = wpilib.Joystick(0)

        self.driveBot = drive.DriveBot.__new__(drive.DriveBot)
        self.driveBot.theRobot = self
        self.driveBot.driverJoystick = self.driverJoystick
        self.driveBot.robotInit()

        self.shooterBot = shooter.MyRobot.__new__(shooter.MyRobot)
        self.shooterBot.theRobot = self
        self.shooterBot.driverJoystick = self.driverJoystick
        self.shooterBot.robotInit()

        self.lifterBot = lifter.Lifter.__new__(lifter.Lifter)
        self.lifterBot.theRobot = self
        self.lifterBot.driverJoystick = self.driverJoystick
        self.lifterBot.robotInit()

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
        yield from sea.parallel(self.driveBot.test(),
                                self.timer(),
                                self.sendLogStatesGenerator())

    def sendLogStatesGenerator(self):
        while True:
            yield
            sea.sendLogStates()

    def teleop(self):
        yield from sea.parallel(
            self.driveBot.teleop(),
            self.wait_mode(),
            self.timer(),
            self.sendLogStatesGenerator())

    def autonomous(self):
        yield from sea.parallel(self.driveBot.autonomous(),
                                self.timer(),
                                self.sendLogStatesGenerator())
    def wait_shootmode(self):
        while not self.driverJoystick.getRawButton(11):
            yield

    def wait_liftmode(self):
        while not self.driverJoystick.getRawButton(12):
            yield

    def wait_mode(self):
        while True:
            yield from sea.watch(self.shooterBot.teleop(),self.wait_liftmode())
            yield from sea.watch(self.lifterBot.teleop(),self.wait_shootmode())
if __name__ == "__main__":
    wpilib.run(MainRobot)
