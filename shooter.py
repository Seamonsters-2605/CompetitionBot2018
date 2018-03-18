import wpilib
import ctre
import seamonsters as sea
import auto_driving
import math

class MyRobot(sea.GeneratorBot):

    def robotInit(self):
        self.leftBelt = ctre.WPI_TalonSRX(4)
        self.rightBelt = ctre.WPI_TalonSRX(5)
        self.leftintake = ctre.WPI_TalonSRX(9)
        self.rightintake = ctre.WPI_TalonSRX(8)
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
                    self.leftintake.set(-0.35)
                    self.rightintake.set(-0.35)
                elif pov == 180:
                    self.leftBelt.set(-.45)
                    self.rightBelt.set(-.45)
                    self.rightintake.set(0.7)
                    self.leftintake.set(0.7)
                elif pov == 90:
                    self.leftintake.set(-0.45)
                    self.rightintake.set(0.45)
                    while self.driverJoystick.getPOV() == 90:
                        yield
                    self.leftintake.set(-0.35)
                    self.rightintake.set(-0.35)
                    yield from sea.wait(30)
                    self.leftintake.set(0)
                    self.rightintake.set(0)
                elif pov == 270:
                    self.leftintake.set(0.45)
                    self.rightintake.set(-0.45)
                    while self.driverJoystick.getPOV() == 270:
                        yield
                    self.leftintake.set(-0.35)
                    self.rightintake.set(-0.35)
                    yield from sea.wait(30)
                    self.leftintake.set(0)
                    self.rightintake.set(0)
                else:
                    self.leftBelt.set(0)
                    self.rightBelt.set(0)
                    self.leftintake.set(0)
                    self.rightintake.set(0)
                yield
        finally:
            self.leftBelt.set(0)
            self.rightBelt.set(0)

    def stop(self):
        self.leftBelt.set(0)
        self.rightBelt.set(0)

    def shootGenerator(self):
        self.leftBelt.set(0.8)
        self.rightBelt.set(0.8)
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
        self.rightintake.set(0.35)
        self.leftintake.set(0.35)
        try:
            self.teleopLock = True
            while True:
                yield
        finally:
            self.teleopLock = False
            self.leftBelt.set(0)
            self.rightBelt.set(0)
            #self.rightintake.set(0)
            #self.leftintake.set(0)

    def prepGenerator(self):
        self.rightintake.set(.5)
        self.leftintake.set(.5)
        try:
            yield from sea.forever()
        finally:
            self.rightintake.set(0)
            self.leftintake.set(0)

    def dropWhileDrivingGenerator(self, drive):
        yield from sea.watch(
            auto_driving.driveContinuous(drive, 0.1, math.pi / 2, 0),
            self.dropGenerator())

    def dropWhileDrivingGeneratorVoltage(self, drive):
        yield from sea.watch(
            auto_driving.driveContinuous(drive, 0.3, math.pi / 2, 0),
            self.dropGenerator())

if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)

