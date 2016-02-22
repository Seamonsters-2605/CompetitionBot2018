__author__ = 'Dawson'
import wpilib
class Flywheels():

    def __init__(self, left, right):
        self.Left = left
        self.Right = right
        self.Right.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.Left.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.MaxVelocity = 2000
        self.Left.setPID(1, 0.0009, 1, 0.0) # Zero F's given...
        self.Right.setPID(1, 0.0009, 1, 0.0)
        self.DesiredSpeed = 0
        self.AutoVelocity = self.MaxVelocity
        self.invert = 1

        #self.Left.enableBrakeMode(True)
        #self.Right.enableBrakeMode(True)

    def invertFlywheels(self):
        self.invert *= -1

    def driveVoltage(self, speed):
        if not self.Left.getControlMode() == wpilib.CANTalon.ControlMode.PercentVbus:
            self.Left.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        if not self.Right.getControlMode() == wpilib.CANTalon.ControlMode.PercentVbus:
            self.Right.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        self.Right.set(-speed)
        self.Left.set(speed)
        #print("Speed Left: " + str(self.Left.getEncVelocity()))
        #print("Speed Right: " + str(self.Right.getEncVelocity()))

    def driveSpeed(self, speed):
        self.DesiredSpeed = speed
        if not self.Left.getControlMode() == wpilib.CANTalon.ControlMode.Speed:
            self.Left.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        if not self.Right.getControlMode() == wpilib.CANTalon.ControlMode.Speed:
            self.Right.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.Left.set(speed * self.invert)
        self.Right.set(-speed * self.invert)
        #print("Left Speed: " + str(self.Left.getEncVelocity()))
        #print("Set Speed: " + str(speed * self.MaxVelocity * self.invert))

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