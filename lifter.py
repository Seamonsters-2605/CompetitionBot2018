import wpilib
import ctre
import seamonsters as sea

WING_SPEED = .75
MAX_WING_SPEED = 1.0
CURRENT_LIMIT = 11

class Lifter(sea.GeneratorBot):

    def robotInit(self):
        self.leftWing = ctre.WPI_TalonSRX(6)
        self.leftWing.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.rightWing = ctre.WPI_TalonSRX(7)
        self.rightWing.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.QuadEncoder, 0, 0)
        try:
            self.driverJoystick
        except AttributeError:
            self.driverJoystick = wpilib.Joystick(0)
        self.leftWingLog = sea.LogState("Wing L")
        self.rightWingLog = sea.LogState("Wing R")

    def teleop(self):
        yield from sea.parallel(
            # clockwise
            self.wingGenerator(self.leftWing, motorReverse=-1, button=5, axis=4,
                               axisReverse=1, log=self.leftWingLog),
            # counter-clockwise
            self.wingGenerator(self.rightWing, motorReverse=1, button=4, axis=1,
                               axisReverse=-1, log=self.rightWingLog))

    def wingGenerator(self, motor, motorReverse, button, axis, axisReverse, log):
        try:
            while not self.driverJoystick.getRawButton(button):
                log.update("Ready to release")
                yield
            motor.set(WING_SPEED * motorReverse)
            for _ in range(30):
                log.update("Releasing")
                yield
            motor.set(0)
            while self.driverJoystick.getRawButton(button):
                log.update("Released")
                yield
            while True:
                while not self.driverJoystick.getRawButton(button):
                    log.update("Ready")
                    yield
                while self.driverJoystick.getRawButton(button):
                    speed = WING_SPEED
                    axisValue = self.driverJoystick.getRawAxis(axis) * axisReverse
                    if axisValue > 0:
                        speed += (1 - speed) * axisValue
                    else:
                        speed *= axisValue + 1
                    motor.set(speed * motorReverse)
                    current = motor.getOutputCurrent()
                    log.update(current)
                    if current > CURRENT_LIMIT:
                        while self.driverJoystick.getRawButton(button):
                            log.update("Current limit!")
                            yield
                        while not self.driverJoystick.getRawButton(button):
                            log.update("Current limit!")
                            yield
                        break
                    yield
                motor.set(0)
        finally:
            motor.set(0)


if __name__ == "__main__":
    wpilib.run(Lifter, physics_enabled=True)
