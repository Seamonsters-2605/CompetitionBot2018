import wpilib
import ctre
import seamonsters as sea

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

    def teleop(self):
        try:
            while True:
                pov = self.driverJoystick.getPOV()
                if self.driverJoystick.getRawButton(2):
                    self.leftBelt.set(1)
                    self.rightBelt.set(1)
                elif pov == 0 or self.driverJoystick.getRawButton(1):
                    self.leftBelt.set(0.55)
                    self.rightBelt.set(0.55)
                    self.leftintake.set(0.8)
                    self.rightintake.set(0.8)
                elif pov == 180:
                    self.leftBelt.set(-0.25)
                    self.rightBelt.set(-0.25)
                    self.rightintake.set(-0.25)
                    self.leftintake.set(-0.25)
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
        self.leftBelt.set(0.45)
        self.rightBelt.set(0.45)
        try:
            for i in range(70):
                yield
        finally:
            self.leftBelt.set(0)
            self.rightBelt.set(0)

    def dropGenerator(self):
        self.leftBelt.set(-0.25)
        self.rightBelt.set(-0.25)
        try:
            for i in range(70):
                yield
        finally:
            self.leftBelt.set(0)
            self.rightBelt.set(0)

if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)

