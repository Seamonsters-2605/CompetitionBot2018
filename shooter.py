import wpilib
import ctre
import seamonsters as sea

class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.leftBelt = ctre.WPI_TalonSRX(4)
        self.rightBelt = ctre.WPI_TalonSRX(5)
        self.joystick = wpilib.Joystick(1)

    def teleopPeriodic(self):
        self.leftBelt.set(self.joystick.getRawAxis(2) * 0.2)
        self.rightBelt.set(self.joystick.getRawAxis(1) * 0.2)

        if(self.joystick.getRawButton(1)):
            self.leftBelt.set(1)
            self.rightBelt.set(1)
            for i in range(50):
                yield

        if(self.joystick.getRawButton(2)):
            self.leftBelt.set(0.2)
            self.rightBelt.set(0.2)
            for i in range(50):
                yield

        if(self.joystick.getRawButton(4)):
            self.leftBelt.set(-0.2)
            self.rightBelt.set(-0.2)
            for i in range(50):
                yield

if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)

