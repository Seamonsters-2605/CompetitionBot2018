import wpilib

class SeizureLitesSpazzzm (wpilib.IterativeRobot):
    def robotInit(self):
        self.joystick = wpilib.Joystick(0)
        self.output = wpilib.DigitalOutput(0)
        self.output.set(False)
    def teleopPeriodic(self):
        if self.joystick.getRawButton(1):
            self.output.set(True)
print ("EnAbLiNg LiGhTiNg")

if __name__ == "__main__":
    wpilib.run(SeizureLitesSpazzzm, physics_enabled=True)


#whoo comments they're really helpful














































#psyche
