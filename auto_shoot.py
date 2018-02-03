import ctre
import wpilib
import seamonsters as sea

class AutoTestRobot(sea.GeneratorBot):

    def robotInit(self):
        self.left = ctre.WPI_TalonSRX(4)
        self.right = ctre.WPI_TalonSRX(5)

    def shootMotor(self, speed, count):
        self.left.set(speed)
        self.right.set(speed)
        for i in range(count):
            yield
        self.left.set(0)
        self.right.set(0)

    def teleop(self):
        yield from self.shootMotor(1, 200)


if __name__ == "__main__":
    wpilib.run(AutoTestRobot, physics_enabled=True)