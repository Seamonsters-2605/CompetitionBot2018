import wpilib
import ctre
import seamonsters as sea

class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.leftBelt = ctre.WPI_TalonSRX(4)
        self.rightBelt = ctre.WPI_TalonSRX(5)

    def teleopPeriodic(self):
        pov = self.driverJoystick.getPOV()
        if self.driverJoystick.getRawButton(2):
            self.leftBelt.set(1)
            self.rightBelt.set(1)
        elif pov == 0:
            self.leftBelt.set(0.4)
            self.rightBelt.set(0.4)
        elif pov == 180:
            self.leftBelt.set(-0.15)
            self.rightBelt.set(-0.15)
        else:
            self.leftBelt.set(0)
            self.rightBelt.set(0)

    def shootGenerator(self):
        self.leftBelt.set(0.4)
        self.rightBelt.set(0.4)
        for i in range(70):
            yield
        self.leftBelt.set(0)
        self.rightBelt.set(0)

if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)

