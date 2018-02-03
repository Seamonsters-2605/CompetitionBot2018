import math

theRobot = "2018"

wheelCircumference = 6 * math.pi

if theRobot == "Leviathan":
    # encoder has 100 raw ticks -- with a QuadEncoder that makes 400 ticks
    # the motor gear has 12 teeth and the wheel has 85 teeth
    # 85 / 12 * 400 = 2833.333 = ~2833
    ticksPerWheelRotation = 2833
    maxError = ticksPerWheelRotation * 1.5
    magnitudeScale = 0.45
    turnScale = 0.3
    maxVelocityPositionMode = 650
    maxVelocitySpeedMode = maxVelocityPositionMode * 5

    positionToSpeedFeedForward = 0.0

    # PIDF values for fast driving:
    fastPID = (1.0, 0.0009, 3.0, 0.0)
    fastPIDSpeedMode = (1.0, 0.0009, 3.0, 0.0)
    # speed at which fast PID's should be used:
    fastPIDScale = 0.09
    # PIDF values for slow driving:
    slowPID = (30.0, 0.0009, 3.0, 0.0)
    slowPIDSpeedMode = (3.0, 0.0009, 3.0, 0.0)
    # speed at which slow PID's should be used:
    slowPIDScale = 0.01

    # for auto switching between position and speed mode
    speedModeThreshold = 0.05
elif theRobot == "2018":
    ticksPerWheelRotation = 20896
    maxError = ticksPerWheelRotation * 1.5
    magnitudeScale = 1.0
    turnScale = 0.5
    maxVelocityPositionMode = 6000 * .8
    maxVelocitySpeedMode = 10000 * .8

    # somewhere between 0.1 and 0.5?
    #positionToSpeedFeedForward = 0.3
    positionToSpeedFeedForward = 0.0

    # PIDF values for fast driving:
    fastPID = (0.07, 0.0, 3.0, 0.0)
    fastPIDSpeedMode = [0.1, 0.0009, 3.0, 0.0]
    # speed at which fast PID's should be used:
    fastPIDScale = 0.09
    # PIDF values for slow driving:
    slowPID = (1.5, 0.0, 3.0, 0.0)
    slowPIDSpeedMode = (1.0, 0.0009, 3.0, 0.0)
    # speed at which slow PID's should be used:
    slowPIDScale = 0.01

    # for auto switching between position and speed mode
    speedModeThreshold = 0.15
