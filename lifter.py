import wpilib
import ctre
import seamonsters as sea

WING_SPEED = .75
CURRENT_LIMIT = 11

class Lifter(sea.GeneratorBot):

    def robotInit(self):
        self.leftWing = ctre.WPI_TalonSRX(6)
        self.rightWing = ctre.WPI_TalonSRX(7)
        try:
            self.driverJoystick
        except AttributeError:
            self.driverJoystick = wpilib.Joystick(0)

    def teleop(self):
        leftWingRunning = True
        rightWingRunning = True
        try:
            while True:
                if leftWingRunning:
                    current = self.leftWing.getOutputCurrent()
                    print(current)
                    if current > CURRENT_LIMIT:
                        self.leftWing.set(0)
                        leftWingRunning = False
                    elif self.driverJoystick.getRawButton(5):
                        self.leftWing.set(-WING_SPEED)
                    elif self.driverJoystick.getRawButton(9):
                        self.leftWing.set(WING_SPEED)
                    else:
                        self.leftWing.set(0)
                else:
                    self.leftWing.set(0)
                    print("no left wing!!!")

                if rightWingRunning:
                    current = self.rightWing.getOutputCurrent()
                    print(current)
                    if current > CURRENT_LIMIT:
                        self.rightWing.set(0)
                        rightWingRunning = False
                    elif self.driverJoystick.getRawButton(4):
                        self.rightWing.set(-WING_SPEED)
                    elif self.driverJoystick.getRawButton(3):
                        self.rightWing.set(WING_SPEED)
                    else:
                        self.rightWing.set(0)
                else:
                    self.rightWing.set(0)
                    print("no right wing!!!")

                if self.driverJoystick.getRawButton(8):
                    leftWingRunning = True
                    rightWingRunning = True

                yield
        finally:
            self.leftWing.set(0)
            self.rightWing.set(0)


if __name__ == "__main__":
    wpilib.run(Lifter, physics_enabled=True)
