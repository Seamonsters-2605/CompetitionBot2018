import wpilib
import seamonsters as sea
import ctre
import math
from robotpy_ext.common_drivers.navx import AHRS
class MyRobot(sea.GeneratorBot):
    def robotInit(self):
        self.joystick = wpilib.Joystick(0)
        self.fl = ctre.WPI_TalonSRX(2)
        self.fr = ctre.WPI_TalonSRX(1)
        self.bl = ctre.WPI_TalonSRX(0)
        self.br = ctre.WPI_TalonSRX(3)
        self.talons = [self.fl,self.fr,self.bl, self.br]
        self.ahrs = AHRS.create_spi()
        self.holoDrive = sea.HolonomicDrive(self.fl, self.fr, self.bl, self.br, 1)
        self.holoDrive.invert

    def teleop(self):
        x = self.joystick.getX()
        y = self.joystick.getY()
        turn = self.joystick.getTwist()
        thrust = self.joystick.getZ()
        b = self.joystick.getRawButton(1)
        a = self.joystick.getMagnitude()
        print("x = {}  y = {}  turn = {} thrust = {} b = {} a ={} ".format(x,y,turn,thrust,b,a))
        # MoveStraight Forward Sself.holoDrive.drive(1,1.58,0)

        if x +- .2:
            self.holoDrive.drive(y,1.58,0)

        if y +- .2:
            self.holoDrive.drive(x,0,0)
        '''if x != 0 and y != 0:
            angle = math.atan(y / x)
            self.holoDrive.drive(thrust,0,angle)
        if y == 0:
            self.holoDrive.drive(x,0,0)'''


    def autonomous(self):
        self.holoDrive.drive(0.5,0,0)

if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)