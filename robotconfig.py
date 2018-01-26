theRobot = "2018"

if theRobot == "Leviathan":
    # encoder has 100 raw ticks -- with a QuadEncoder that makes 400 ticks
    # the motor gear has 12 teeth and the wheel has 85 teeth
    # 85 / 12 * 400 = 2833.333 = ~2833
    ticksPerWheelRotation = 2833
    magnitudeScale = 0.45
    turnScale = 0.3
    maxVelocity = 650

    # PIDF values for fast driving:
    fastPID = (1.0, 0.0009, 3.0, 0.0)
    # speed at which fast PID's should be used:
    fastPIDScale = 0.09
    # PIDF values for slow driving:
    slowPID = (30.0, 0.0009, 3.0, 0.0)
    slowPIDSpeedMode = (3.0, 0.0009, 3.0, 0.0)
    # speed at which slow PID's should be used:
    slowPIDScale = 0.01
elif theRobot == "2018":
    ticksPerWheelRotation = 83584
    magnitudeScale = .45
    turnScale = .3
    maxVelocity = 19177

    # PIDF values for fast driving:
    fastPID = (0.1, 0.0009, 3.0, 0.0)
    fastPIDSpeedMode = (0.05, 0.0009, 3.0, 0.0)
    # speed at which fast PID's should be used:
    fastPIDScale = 0.09
    # PIDF values for slow driving:
    slowPID = (0.5, 0.0009, 3.0, 0.0)
    slowPIDSpeedMode = (0.1, 0.0009, 3.0, 0.0)
    # speed at which slow PID's should be used:
    slowPIDScale = 0.01
