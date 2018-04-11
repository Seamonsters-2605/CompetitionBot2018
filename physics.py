__author__ = "jacobvanthoog"
import math
import wpilib
import inspect, os
import configparser
from pyfrc.physics import drivetrains
from pyfrc.physics.visionsim import VisionSim
import ctre
import robotpy_ext.common_drivers.navx
from networktables import NetworkTables

# make the NavX work with the physics simulator
def createAnalogGyro():
    return wpilib.AnalogGyro(0)
robotpy_ext.common_drivers.navx.AHRS.create_spi = createAnalogGyro

class SimulatedTalon:

    def __init__(self, name):
        if name == '':
            self.port = None
        else:
            self.port = abs(int(name))
        self.inv = -1 if name.startswith('-') else 1
        self.lastPosition = 0

    def getSpeed(self, data, maxVel):
        if self.port == None:
            return 0.0
        try:
            talonData = data['CAN'][self.port]
            controlMode = talonData['control_mode']
            if controlMode == ctre.ControlMode.PercentOutput:
                value = talonData['value']
                if value < -1:
                    value = -1.0
                if value > 1:
                    value = 1.0
                return value * self.inv
            elif controlMode == ctre.ControlMode.Position:
                targetPos = talonData['pid0_target']
                diff = targetPos - self.lastPosition
                self.lastPosition = targetPos
                talonData['quad_position'] = targetPos # update encoders
                return diff / maxVel * 5 * self.inv
            elif controlMode == ctre.ControlMode.Velocity:
                targetVel = talonData['pid0_target']
                talonData['quad_position'] += int(targetVel/5) # update encoders
                return targetVel / maxVel * self.inv
            else:
                return 0.0
        except KeyError:
            return 0.0

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

        self.flMotor = SimulatedTalon(physics.get('canfl', '0'))
        self.frMotor = SimulatedTalon(physics.get('canfr', '0'))
        self.blMotor = SimulatedTalon(physics.get('canbl', '0'))
        self.brMotor = SimulatedTalon(physics.get('canbr', '0'))

        self.maxVel = int(physics.get('maxvel', '8000'))

        ds = config['ds']
        location = int(ds.get('location', '1'))
        team = 1 if (ds.get('team', 'red').lower() == 'blue') else 0
        self.allianceStation = location - 1 + team * 3

        field = config['field']
        self.visionX = float(field.get('visionx', '0'))
        self.visionY = float(field.get('visiony', '0'))
        self.visionAngleStart = float(field.get('visionanglestart', '90'))
        self.visionAngleEnd = float(field.get('visionangleend', '270'))

    def initialize(self, hal_data):
        self.visionTable = NetworkTables.getTable('limelight')
        self.visionTable.putNumber('tv', 1)
        self.visionTable.putNumber('tx', 0)
        self.visionTable.putNumber('ty', 0)
        self.visionTable.putNumber('ts', 0)
        self.visionTable.putNumber('ta', 5)

        visionTarget = VisionSim.Target(self.visionX, self.visionY,
                                        self.visionAngleStart,
                                        self.visionAngleEnd)
        self.visionSim = VisionSim([visionTarget], 60, 2, 50)
        hal_data['alliance_station'] = self.allianceStation

    def update_sim(self, data, time, elapsed):

        fl = self.flMotor.getSpeed(data, self.maxVel)
        fr = self.frMotor.getSpeed(data, self.maxVel)
        bl = self.blMotor.getSpeed(data, self.maxVel)
        br = self.brMotor.getSpeed(data, self.maxVel)

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

        x, y, angle = self.physicsController.get_position()
        visionData = self.visionSim.compute(time, x, y, angle)
        if visionData is not None:
            targetData = visionData[0]
            self.visionTable.putNumber('tv', targetData[0])
            if targetData[0] != 0:
                self.visionTable.putNumber('tx', targetData[2])
        else:
            # DOESN'T mean no vision. vision just doesn't always update
            pass
