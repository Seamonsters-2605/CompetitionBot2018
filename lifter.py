import wpilib
import ctre
import seamonsters as sea
class Lifter():

    def robotInit(self):
        self.leftWing = ctre.WPI_TalonSRX()
        self.rightWing = ctre.WPI_TalonSRX()
        self.joystick = wpilib.Joystick(1)

    def Lift(self):
        if(self.joystick.getRawButton(9)):
            self.leftWing.set(1)
        if(self.joystick.getRawButton(10)):
            self.leftWing.set(1)

if __name__ == "__main__":
    wpilib.run(Lifter, physics_enabled=True)
