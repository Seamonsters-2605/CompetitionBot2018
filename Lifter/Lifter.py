import wpilib

class Lifter():
    def __init__(self):
        self.leftLift = wpilib.Talon(0)
        self.rightLift = wpilib.Talon(1)
        self.tapeMeasurer = wpilib.Talon(2)
        self.left = 1
        self.right = -1
    def liftUp(self):
        self.left = -1
        self.right = -1
        self.tapeMeasurer.set(.2)
        self.leftLift.set(self.left)
        self.rightLift.set(self.right)
    def pullUp(self):
        self.right = 1
        self.left = 1
        self.leftLift.set(self.left)
        self.rightLift.set(self.right)
