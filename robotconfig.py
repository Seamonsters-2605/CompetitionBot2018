import math

theRobot = "2018"

wheelCircumference = 6 * math.pi

if theRobot == "Leviathan":
    # encoder has 100 raw ticks -- with a QuadEncoder that makes 400 ticks
    # the motor gear has 12 teeth and the wheel has 85 teeth
    # 85 / 12 * 400 = 2833.333 = ~2833
    ticksPerWheelRotation = 2833
    maxError = ticksPerWheelRotation * 1.5
    maxVelocityPositionMode = 650
    maxVelocitySpeedMode = maxVelocityPositionMode * 5

    positionModePIDs = (
        (30.0, 0.0009, 3.0, 0.0),
        (1.0, 0.0009, 3.0, 0.0),
        (1.0, 0.0009, 3.0, 0.0)
    )
    speedModePIDs = (
        (3.0, 0.0009, 3.0, 0.0),
        (1.0, 0.0009, 3.0, 0.0),
        (1.0, 0.0009, 3.0, 0.0)
    )
elif theRobot == "2018":
    ticksPerWheelRotation = 20896
    maxError = ticksPerWheelRotation * 1.5
    maxVelocityPositionMode = 6000 * .8
    maxVelocitySpeedMode = 10000 * .8

    positionModePIDs = (
        (0.8, 0.0, 10.0, 0.0), # slow
        (0.07, 0.0, 3.0, 0.0), # medium
        (0.07, 0.0, 3.0, 0.0) # fast
    )
    speedModePIDs = (
        (1.0, 0.0009, 3.0, 0.0), # slow
        (0.1, 0.0009, 3.0, 0.0), # medium
        (0.1, 0.0009, 3.0, 0.0) # fast
    )
