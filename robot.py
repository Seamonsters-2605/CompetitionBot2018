import wpilib
import seamonsters as sea
import drive
import shooter

class MainRobot(sea.GeneratorBot):

    def robotInit(self):
        self.driveObject = drive.DriveBot.__new__(drive.DriveBot)
        drive.DriveBot.robotInit(self.driveObject)
        self.shooterInstance = sea.IterativeRobotInstance(shooter.MyRobot)

    def teleop(self):
        yield from sea.parallel(drive.DriveBot.teleop(self.driveObject),
                                self.shooterInstance.teleopGenerator())

if __name__ == "__main__":
    wpilib.run(MainRobot)
