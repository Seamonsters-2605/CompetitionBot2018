__author__ = "jacobvanthoog"
import math
import wpilib
import inspect, os
import configparser
from pyfrc.physics import drivetrains
import ctre
import robotpy_ext.common_drivers.navx

# make the NavX work with the physics simulator
def createAnalogGyro():
    return wpilib.AnalogGyro(0)
robotpy_ext.common_drivers.navx.AHRS.create_spi = createAnalogGyro

class PhysicsEngine:

    def __init__(self, physicsController):
        self.physicsController = physicsController

        # NavX simulation
        self.physicsController.add_analog_gyro_channel(0)

        config = configparser.ConfigParser()
        filename = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + os.sep + "sim" + os.sep + "drivetrain.ini"
        print("Reading robot data from", filename)
        config.read(filename)

        if not 'physics' in config:
            print("Please use the [physics] header in drivetrain.ini")
            exit()
        physics = config['physics']
        # get() allows fallback values if the key isn't in the config file
        self.xLen = float(physics.get('xlen', '2'))
        self.yLen = float(physics.get('ylen', '3'))
        self.speed = float(physics.get('speed', '6'))
        self.drivetrain = physics.get('drivetrain', 'four')

        flName = physics.get('canfl', '0')
        self.canFL = abs(int(flName))
        self.canFLInv = -1 if flName.startswith('-') else 1

        frName = physics.get('canfr', '0')
        self.canFR = abs(int(frName))
        self.canFRInv = -1 if frName.startswith('-') else 1

        blName = physics.get('canbl', '0')
        self.canBL = abs(int(blName))
        self.canBLInv = -1 if blName.startswith('-') else 1

        brName = physics.get('canbr', '0')
        self.canBR = abs(int(brName))
        self.canBRInv = -1 if brName.startswith('-') else 1

    def initialize(self, hal_data):
        pass

    def _readMotor(self, data, motor):
        controlMode = data['CAN'][motor]['control_mode']
        if controlMode != ctre.ControlMode.PercentOutput:
            return 0.0
        value = data['CAN'][motor]['value']
        if value < -1:
            value = -1.0
        if value > 1:
            value = 1.0
        return value

    def update_sim(self, data, time, elapsed):
        # read CAN data to get motor speeds
        try:
            fl = self._readMotor(data, self.canFL) * self.canFLInv
            fr = self._readMotor(data, self.canFR) * self.canFRInv
            if not self.drivetrain == "two":
                bl = self._readMotor(data, self.canBL) * self.canBLInv
                br = self._readMotor(data, self.canBR) * self.canBRInv
        except KeyError:
            return

        if self.drivetrain == "mecanum":
            vx, vy, vw = drivetrains.mecanum_drivetrain(bl, br, fl, fr,
                self.xLen, self.yLen, self.speed)
            self.physicsController.vector_drive(vx, vy, vw, elapsed)
        elif self.drivetrain == "four":
            speed, rot = drivetrains.four_motor_drivetrain(bl, br, fl, fr,
                self.xLen, self.speed)
            self.physicsController.drive(speed, rot, elapsed)
        elif self.drivetrain == "two":
            speed, rot = drivetrains.two_motor_drivetrain(fl, fr,
                self.xLen, self.speed)
            self.physicsController.drive(speed, rot, elapsed)

        # https://github.com/robotpy/robotpy-wpilib/issues/291
        data['analog_gyro'][0]['angle'] = math.degrees(self.physicsController.angle)
