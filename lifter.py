import wpilib
import ctre
import seamonsters as sea

class Lifter():

    def robotInit(self):
        self.leftWing = ctre.WPI_TalonSRX(6)
        self.rightWing = ctre.WPI_TalonSRX(7)
        self.joystick = wpilib.Joystick(1)

    def Lift(self):
        if(self.joystick.getRawButton(9)):
            self.leftWing.set(1)
        if(self.joystick.getRawButton(10)):
            self.rightWing.set(1)
        else:
            self.leftWing.set(0)
            self.rightWing.set(0)

if __name__ == "__main__":
    wpilib.run(Lifter, physics_enabled=True)
