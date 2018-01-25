theRobot = "Leviathan"

if theRobot == "Leviathan":
    # encoder has 100 raw ticks -- with a QuadEncoder that makes 400 ticks
    # the motor gear has 12 teeth and the wheel has 85 teeth
    # 85 / 12 * 400 = 2833.333 = ~2833
    ticksPerWheelRotation = 2833
    magnitudeScale = 0.45
    turnScale = 0.3
    maxVelocity = 650
elif theRobot == "2018":
    ticksPerWheelRotation = 83584
    magnitudeScale = 1.0
    turnScale = 1.0
    maxVelocity = 650
