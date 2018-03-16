import math

theRobot = "2018 new encoders"

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
    maxError = ticksPerWheelRotation * 1.5
    maxVelocityPositionMode = maxVelocitySpeedMode / 5

    positionModePIDs = (
        (0.4, 0.0, 10.0, 0.0), # slow
        (0.6, 0.0, 5.0, 0.0), # medium
        (0.07, 0.0, 3.0, 0.0) # fast
    )
    speedModePIDs = (
        (0.1, 0.0009, 3.0, 0.0), # original medium
        (0.8, 0.0, 10.0, 0.0), # new/special
        (0.1, 0.0009, 3.0, 0.0) # fast (voltage, doesn't matter)
    )
