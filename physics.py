__author__ = "jacobvanthoog"
import wpilib
import inspect, os
import configparser
from pyfrc.physics import drivetrains

class PhysicsEngine:

    def __init__(self, physicsController):
        self.physicsController = physicsController

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

        fl = int(physics.get('canfl', '0'))
        self.canFL = abs(fl)
        self.canFLInv = 1 if fl >= 0 else -1

        fr = int(physics.get('canfr', '0'))
        self.canFR = abs(fr)
        self.canFRInv = 1 if fr >= 0 else -1

        bl = int(physics.get('canbl', '0'))
        self.canBL = abs(bl)
        self.canBLInv = 1 if bl >= 0 else -1

        br = int(physics.get('canbr', '0'))
        self.canBR = abs(br)
        self.canBRInv = 1 if br >= 0 else -1

    def initialize(self, hal_data):
        pass

    def update_sim(self, data, time, elapsed):
        valueName = 'value'
        
        # read CAN data to get motor speeds
        maxValue = 1024
        fl = (data['CAN'][self.canFL][valueName] * self.canFLInv / maxValue)
        fr = (data['CAN'][self.canFR][valueName] * self.canFRInv / maxValue)
        if not self.drivetrain == "two":
            bl = (data['CAN'][self.canBL][valueName] * self.canBLInv / maxValue)
            br = (data['CAN'][self.canBR][valueName] * self.canBRInv / maxValue)

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

