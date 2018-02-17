import wpilib
import ctre

WING_SPEED = .75
CURRENT_LIMIT = 200

class Lifter(wpilib.IterativeRobot):

    def robotInit(self):
        self.leftWing = ctre.WPI_TalonSRX(6)
        self.rightWing = ctre.WPI_TalonSRX(7)
        self.joystick = wpilib.Joystick(0)

    def teleopInit(self):        
        self.leftWingRunning = True
        self.rightWingRunning = True

    def teleopPeriodic(self):
        if self.leftWingRunning:
            current = self.leftWing.getOutputCurrent()
            print(current)
            if current > CURRENT_LIMIT:
                self.leftWing.set(0)
                self.leftWingRunning = False
            elif self.joystick.getRawButton(5):
                self.leftWing.set(-WING_SPEED)
            elif self.joystick.getRawButton(9):
                self.leftWing.set(WING_SPEED)
            else:
                self.leftWing.set(0)
        else:
            self.leftWing.set(0)
            print("no left wing!!!")

        if self.rightWingRunning:
            current = self.rightWing.getOutputCurrent()
            print(current)
            if current > CURRENT_LIMIT:
                self.rightWing.set(0)
                self.rightWingRunning = False
            elif self.joystick.getRawButton(4):
                self.rightWing.set(-WING_SPEED)
            elif self.joystick.getRawButton(3):
                self.rightWing.set(WING_SPEED)
            else:
                self.rightWing.set(0)
        else:
            self.rightWing.set(0)
            print("no right wing!!!")

        if self.joystick.getRawButton(8):
            self.leftWingRunning = True
            self.rightWingRunning = True


if __name__ == "__main__":
    wpilib.run(Lifter, physics_enabled=True)
