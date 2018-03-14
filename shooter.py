import wpilib
import ctre
import seamonsters as sea
import auto_driving
import math

class MyRobot(sea.GeneratorBot):

    def robotInit(self):
        self.leftBelt = ctre.WPI_TalonSRX(4)
        self.rightBelt = ctre.WPI_TalonSRX(5)
        try:
            self.driverJoystick
        except AttributeError:
            self.driverJoystick = wpilib.Joystick(0)
        self.teleopLock = False

    def teleop(self):
        try:
            while True:
                if self.teleopLock:
                    yield
                    continue
                pov = self.driverJoystick.getPOV()
                if self.driverJoystick.getRawButton(2):
                    self.leftBelt.set(1)
                    self.rightBelt.set(1)
                elif pov == 0 or self.driverJoystick.getRawButton(1):
                    self.leftBelt.set(0.55)
                    self.rightBelt.set(0.55)
                elif pov == 180:
                    self.leftBelt.set(-0.25)
                    self.rightBelt.set(-0.25)
                else:
                    self.leftBelt.set(0)
                    self.rightBelt.set(0)
                yield
        finally:
            self.leftBelt.set(0)
            self.rightBelt.set(0)

    def stop(self):
        self.leftBelt.set(0)
        self.rightBelt.set(0)

    def shootGenerator(self):
        self.leftBelt.set(0.45)
        self.rightBelt.set(0.45)
        try:
            self.teleopLock = True
            for i in range(70):
                yield
        finally:
            self.teleopLock = False
            self.leftBelt.set(0)
            self.rightBelt.set(0)

    def dropGenerator(self):
        self.leftBelt.set(-0.25)
        self.rightBelt.set(-0.25)
        try:
            self.teleopLock = True
            while True:
                yield
        finally:
            self.teleopLock = False
            self.leftBelt.set(0)
            self.rightBelt.set(0)

    def dropWhileDrivingGenerator(self, drive):
        yield from sea.watch(
            auto_driving.driveContinuous(drive, 0.1, math.pi / 2, 0),
            self.dropGenerator())

if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)

