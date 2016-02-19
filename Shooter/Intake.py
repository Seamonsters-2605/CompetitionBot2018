__author__ = 'Dawson'
import wpilib
class Intake():

    def __init__(self, intake):
        self.Motor = intake
        self.Invert = -1

    def intakeBall(self):
        self.Motor.set(.75 * self.Invert)

    def dischargeBall(self):
        self.Motor.set(-1 * self.Invert)

    def stop(self):
        self.Motor.set(0)

    def invert(self):
        self.Invert *= -1
