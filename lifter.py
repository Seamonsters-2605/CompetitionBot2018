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
        self.wingGamepad = sea.Gamepad(1)
        self.leftWingLog = sea.LogState("Wing L")
        self.rightWingLog = sea.LogState("Wing R")

    def teleop(self):
        yield from sea.parallel(
            # clockwise
            self.wingGenerator(self.leftWing, motorReverse=-1,
                               button=sea.Gamepad.LT, axis=1,
                               currentOverrideButton=sea.Gamepad.LB,
                               log=self.leftWingLog),
            # counter-clockwise
            self.wingGenerator(self.rightWing, motorReverse=1,
                               button=sea.Gamepad.RT, axis=5,
                               currentOverrideButton=sea.Gamepad.RB,
                               log=self.rightWingLog))

    def wingGenerator(self, motor, motorReverse, button, axis,
                      currentOverrideButton, log):
        try:
            while not self.wingGamepad.getRawButton(button):
                log.update("Ready to release")
                yield
            currentPosition = motor.getSelectedSensorPosition(0)
            # 500 too high
            # 400 slightly too hight
            # 300 barely enough, sometimes not enough
            motor.set(ctre.ControlMode.Position, currentPosition + 350 * motorReverse)
            #motor.set(WING_SPEED * motorReverse)
            #for _ in range(18):
            #    log.update("Releasing")
            #    yield
            #motor.set(0)
            while self.wingGamepad.getRawButton(button):
                log.update("Released")
                yield
            motor.set(0)
            while True:
                while not self.wingGamepad.getRawButton(button):
                    log.update("Ready")
                    yield
                while self.wingGamepad.getRawButton(button):
                    speed = WING_SPEED
                    axisValue = -self.wingGamepad.getRawAxis(axis)
                    if axisValue > 0:
                        speed += (1 - speed) * axisValue
                    else:
                        speed *= axisValue + 1
                    motor.set(speed * motorReverse)
                    current = motor.getOutputCurrent()
                    log.update(current + " " +
                               str(self.wingGamepad.getRawButton(currentOverrideButton)))
                    if current > CURRENT_LIMIT and \
                            (not self.wingGamepad.getRawButton(currentOverrideButton)):
                        motor.set(0)
                        while self.wingGamepad.getRawButton(button):
                            log.update("Current limit!")
                            yield
                        while not self.wingGamepad.getRawButton(button):
                            log.update("Current limit!")
                            yield
                        break
                    yield
                motor.set(0)
        finally:
            motor.set(0)


if __name__ == "__main__":
    wpilib.run(Lifter, physics_enabled=True)
