import wpilib
import ctre
import seamonsters as sea

class Lifter():

    def robotInit(self):
        self.leftWing = ctre.WPI_TalonSRX(6)
        self.rightWing = ctre.WPI_TalonSRX(7)
        self.joystick = wpilib.Joystick(1)

    def teleopInit(self):        
        self.leftWingRunning = True
        self.rightWingRunning = True

    def teleopPeriodic(self):
        print(self.rightWing.getOutputCurrent())
        print(self.leftWing.getOutputCurrent())

        if(self.rightWing.getOutputCurrent() > 200):
            self.rightWingRunning = False
        if(self.leftWing.getOutputCurrent() > 200):
            self.leftWingRunning = False

        if(self.leftWingRunning):
            if(self.joystick.getRawButton(9)):
                self.leftWing.set(1)
            else:
                self.leftWing.set(0)

        if(self.rightWingRunning):
            if(self.joystick.getRawButton(10)):
                self.rightWing.set(1)
            else:
                self.rightWing.set(0)

        if(self.joystick.getRawButton(8)):
            self.leftWingRunning = True
            self.rightWingRunning = True


if __name__ == "__main__":
    wpilib.run(Lifter, physics_enabled=True)
