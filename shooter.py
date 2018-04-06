import wpilib
import ctre
import seamonsters as sea
import auto_driving
import math

INTAKE_SCALE = 1

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

        self.shootLED = wpilib.DigitalOutput(4)

    def teleop(self):
        try:
            while True:
                if self.teleopLock:
                    yield
                    continue
                pov = self.driverJoystick.getPOV()
                if self.driverJoystick.getRawButton(2):
                    self.shootLED.set(True)
                    self.leftBelt.set(1)
                    self.rightBelt.set(1)
                    self.leftintake.set(-0.35 * INTAKE_SCALE)
                    self.rightintake.set(-0.35 * INTAKE_SCALE)
                elif pov == 0 or self.driverJoystick.getRawButton(1):
                    self.shootLED.set(True)
                    self.leftBelt.set(0.55)
                    self.rightBelt.set(0.55)
                    self.leftintake.set(-0.35 * INTAKE_SCALE)
                    self.rightintake.set(-0.35 * INTAKE_SCALE)
                elif pov == 180:
                    self.shootLED.set(True)
                    self.leftBelt.set(-.45)
                    self.rightBelt.set(-.45)
                    self.rightintake.set(0.85 * INTAKE_SCALE)
                    self.leftintake.set(0.85 * INTAKE_SCALE)
                elif pov == 90:
                    self.shootLED.set(True)
                    self.leftintake.set(-0.45 * INTAKE_SCALE)
                    self.rightintake.set(0.45 * INTAKE_SCALE)
                    while self.driverJoystick.getPOV() == 90:
                        yield
                    self.leftintake.set(-0.35 * INTAKE_SCALE)
                    self.rightintake.set(-0.35 * INTAKE_SCALE)
                    yield from sea.wait(30)
                    self.leftintake.set(0)
                    self.rightintake.set(0)
                elif pov == 270:
                    self.shootLED.set(True)
                    self.leftintake.set(0.45 * INTAKE_SCALE)
                    self.rightintake.set(-0.45 * INTAKE_SCALE)
                    while self.driverJoystick.getPOV() == 270:
                        yield
                    self.leftintake.set(-0.35 * INTAKE_SCALE)
                    self.rightintake.set(-0.35 * INTAKE_SCALE)
                    yield from sea.wait(30)
                    self.leftintake.set(0)
                    self.rightintake.set(0)
                else:
                    self.shootLED.set(False)
                    self.leftBelt.set(0)
                    self.rightBelt.set(0)
                    self.leftintake.set(0)
                    self.rightintake.set(0)
                yield
        finally:
            self.leftBelt.set(0)
            self.rightBelt.set(0)

    def stop(self):
        print("Shooter stop()")
        self.leftBelt.set(0)
        self.rightBelt.set(0)

    def shootGenerator(self):
        print("Start shootGenerator")
        self.shootLED.set(True)
        self.leftBelt.set(1.0)
        self.rightBelt.set(1.0)
        self.leftintake.set(-0.35 * INTAKE_SCALE)
        self.rightintake.set(-0.35 * INTAKE_SCALE)
        try:
            self.teleopLock = True
            for i in range(70):
                yield
        finally:
            print("End shootGenerator")
            self.teleopLock = False
            self.leftBelt.set(0)
            self.rightBelt.set(0)
            self.leftintake.set(0)
            self.rightintake.set(0)
            self.shootLED.set(False)

    def dropGenerator(self):
        print("Start dropGenerator")
        self.leftBelt.set(-.45)
        self.rightBelt.set(-.45)
        self.rightintake.set(0.85 * INTAKE_SCALE)
        self.leftintake.set(0.85 * INTAKE_SCALE)
        try:
            self.teleopLock = True
            while True:
                yield
        finally:
            print("End dropGenerator")
            self.teleopLock = False
            self.leftBelt.set(0)
            self.rightBelt.set(0)
            #self.rightintake.set(0)
            #self.leftintake.set(0)

    def prepGenerator(self):
        print("Start prepGenerator")
        self.rightintake.set(.5 * INTAKE_SCALE)
        self.leftintake.set(.5 * INTAKE_SCALE)
        try:
            yield from sea.forever()
        finally:
            print("End prepGenerator")
            self.rightintake.set(0)
            self.leftintake.set(0)

    def dropWhileDrivingGenerator(self, drive):
        print("Start dropWhileDrivingGenerator")
        yield from sea.watch(
            auto_driving.driveContinuous(drive, 0.1, math.pi / 2, 0),
            self.dropGenerator())
        print("End dropWhileDrivingGenerator")

    def dropWhileDrivingGeneratorVoltage(self, drive):
        print("Start dropWhileDrivingGeneratorVoltage")
        yield from sea.watch(
            auto_driving.driveContinuous(drive, 0.3, math.pi / 2, 0),
            self.dropGenerator())
        print("End dropWhileDrivingGeneratorVoltage")

if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)

