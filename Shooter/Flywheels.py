__author__ = 'Dawson'
import wpilib
class Flywheels():

    def __init__(self, left, right):
        self.Left = left
        self.Right = right
        self.Right.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.Left.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.MaxVelocity = 3000
        self.Left.setPID(0.5, 0.0, 2.0, 0.0) # Zero F's given...
        self.Right.setPID(0.5, 0.0, 2.0, 0.0)
        self.DesiredSpeed = 0
        self.AutoVelocity = self.MaxVelocity
        self.invert = 1

    def invertFlywheels(self):
        self.invert *= -1

    def driveSpeed(self, speed):
        self.DesiredSpeed = speed
        self.Left.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.Right.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.Left.set(speed * self.MaxVelocity * self.invert)
        self.Right.set(-speed * self.MaxVelocity * self.invert)

    def driveAuto(self):
        self.driveSpeed(self.AutoVelocity)

    def readyToShoot(self):
        if self.DesiredSpeed == 0:
            return False
        if abs(     (abs(self.Left.getEncVelocity()) - abs(self.DesiredSpeed)) / self.DesiredSpeed) < .25:
            return True
        return False

    def setAutoVelocity(self, velocity):
        self.AutoVelocity = velocity