import math
from ctre import ControlMode

theRobot = "2018 new encoders"

class DriveGear:

    def __init__(self, mode,
                 forwardScale=1.0, strafeScale=1.0, turnScale=1.0,
                 p=0.0, i=0.0, d=0.0, f=0.0):
        self.mode = mode
        self.forwardScale = forwardScale
        self.strafeScale = strafeScale
        self.turnScale = turnScale
        self.p = p
        self.i = i
        self.d = d
        self.f = f

    def __repr__(self):
        return str(self.mode) + " fwd %f str %f trn %f (%f %f %f %f)" \
            % (self.forwardScale, self.strafeScale, self.turnScale,
                 self.p, self.i, self.d, self.f)

if theRobot == "Leviathan":
    wheelCircumference = 6 * math.pi
    # encoder has 100 raw ticks -- with a QuadEncoder that makes 400 ticks
    # the motor gear has 12 teeth and the wheel has 85 teeth
    # 85 / 12 * 400 = 2833.333 = ~2833
    ticksPerWheelRotation = 2833
    maxError = ticksPerWheelRotation * 1.5
    maxVelocityPositionMode = 650
    maxVelocitySpeedMode = maxVelocityPositionMode * 5

    positionModePIDs = (
        (30.0, 0.0009, 3.0, 0.0),
        (3.0, 0.0009, 3.0, 0.0),
        (1.0, 0.0009, 3.0, 0.0)
    )
    speedModePIDs = (
        (3.0, 0.0009, 3.0, 0.0),
        (1.0, 0.0009, 3.0, 0.0),
        (1.0, 0.0009, 3.0, 0.0)
    )
elif theRobot == "2018" or theRobot == "2018 new encoders":
    if theRobot == "2018 new encoders":
        # 10,767; 10,819; 10,832
        ticksPerWheelRotation = 10826
        maxVelocitySpeedMode = 12115
    else:
        ticksPerWheelRotation = 7149
        maxVelocitySpeedMode = 8000

    wheelCircumference = 6 * math.pi
    maxError = ticksPerWheelRotation * 1.5
    maxVelocityPositionMode = maxVelocitySpeedMode / 5

    normalGears = (
        DriveGear(mode=ControlMode.Velocity,
                  forwardScale=0.4, strafeScale=0.15, turnScale=0.2,
                  p=0.25, i=0.0, d=5.0),
        DriveGear(mode=ControlMode.Velocity,
                  forwardScale=0.5, strafeScale=0.2, turnScale=0.4,
                  p=0.25, i=0.0, d=5.0),
        DriveGear(mode=ControlMode.Velocity,
                  forwardScale=0.6, strafeScale=0.2, turnScale=0.5,
                  p=0.1, i=0.0009, d=3.0),
    )

    slowPIDGears = (
        DriveGear(mode=ControlMode.Velocity,
                  forwardScale=0.4, strafeScale=0.15, turnScale=0.2,
                  p=0.1, i=0.0009, d=3.0),
        DriveGear(mode=ControlMode.Velocity,
                  forwardScale=0.5, strafeScale=0.2, turnScale=0.4,
                  p=0.1, i=0.0009, d=3.0),
        DriveGear(mode=ControlMode.Velocity,
                  forwardScale=0.6, strafeScale=0.2, turnScale=0.5,
                  p=0.1, i=0.0009, d=3.0)
    )

    voltageGears = (
        DriveGear(mode=ControlMode.PercentOutput,
                  forwardScale=0.5, strafeScale=0.6, turnScale=0.4),
        DriveGear(mode=ControlMode.PercentOutput,
                  forwardScale=0.5, strafeScale=0.6, turnScale=0.4),
        DriveGear(mode=ControlMode.PercentOutput,
                  forwardScale=1.0, strafeScale=0.6, turnScale=0.4)
    )

    autoGear = DriveGear(mode=ControlMode.Velocity,
                         p=0.4, i=0.0, d=10.0)

    autoGearVoltage = DriveGear(mode=ControlMode.PercentOutput)
