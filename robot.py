import wpilib
import seamonsters as sea
import ctre
from robotpy_ext.common_drivers.navx import AHRS
class MyRobot(sea.GeneratorBot):
    def robotInit(self):
        self.fl = ctre.WPI_TalonSRX(2)
        self.fr = ctre.WPI_TalonSRX(1)
        self.bl = ctre.WPI_TalonSRX(0)
        self.br = ctre.WPI_TalonSRX(3)
        self.ahrs = AHRS.create_spi()
    def teleop(self):
        yield from sea.parallel(self.move(),self.write())
    def move(self):
        yield from sea.wait(50)
        yield from sea.timeLimit(self.driveforward(1,100),100)
        yield from sea.wait(100)
        yield from sea.timeLimit(self.driveforward(-1,100),100)
        yield from self.rotate(40)
        yield from sea.timeLimit(self.write(),500)

    def driveforward(self,speed,time):
        self.fl.set(-speed)
        self.fr.set(speed)
        self.bl.set(-speed)
        self.br.set(speed)
        try:
            while True:
                yield
        finally:
            self.fl.set(0)
            self.fr.set(0)
            self.bl.set(0)
            self.br.set(0)

    def rotate(self,angle):
        currentAngle = self.ahrs.getAngle()
        targetAngle = currentAngle + angle
        self.fl.set(-1)
        self.fr.set(-1)
        self.bl.set(-1)
        self.br.set(-1)
        while targetAngle > self.ahrs.getAngle() :
            yield
        self.fl.set(0)
        self.fr.set(0)
        self.bl.set(0)
        self.br.set(0)
    def write(self):
        while True:
            print('hello')
            yield from sea.wait(50)


if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)