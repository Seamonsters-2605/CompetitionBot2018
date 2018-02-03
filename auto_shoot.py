import ctre
class Shooter():

    def __init__(self):
        self.left = ctre.WPI_TalonSRX(4)
        self.right = ctre.WPI_TalonSRX(5)

    def shootMotor(self, speed, count):
        self.left.set(speed)
        self.right.set(speed)
        for i in range(count):
            yield
        self.left.set(0)
        self.right.set(0)