import wpilib
import seamonsters as sea
import drive
import shooter

class MainRobot(sea.GeneratorBot):

    def robotInit(self):
        self.driveObject = drive.DriveBot.__new__(drive.DriveBot)
        drive.DriveBot.robotInit(self.driveObject)
        self.shooterInstance = sea.IterativeRobotInstance(shooter.MyRobot)
        self.timerLogState = sea.LogState("Time")

    def timer(self):
        i = 0
        while True:
            i += 1
            self.timerLogState.update(i // 50)
            yield

    def teleop(self):
        yield from sea.parallel(drive.DriveBot.teleop(self.driveObject),
                                self.shooterInstance.teleopGenerator(),
                                self.timer())

    def autonomous(self):
        yield from sea.parallel(drive.DriveBot.autonomous(self.driveObject),
                                self.timer())

if __name__ == "__main__":
    wpilib.run(MainRobot)
