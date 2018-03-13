import wpilib

class SeizureLitesSpazzzm (wpilib.IterativeRobot):
    def robotInit(self):
        self.joystick = wpilib.Joystick(0)
        wpilib.DigitalOutput(0)
        wpilib.DigitalOutput.enablePWM(0)
    def teleopPeriodic(self):
        if self.joystick.getRawButton(1):
            wpilib.DigitalOutput.disablePWM()
print ("Whoo")

if __name__ == "__main__":
    wpilib.run(SeizureLitesSpazzzm, physics_enabled=True)


#whoo comments they're really helpful














































#psyche
