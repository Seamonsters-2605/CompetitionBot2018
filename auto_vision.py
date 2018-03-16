import seamonsters as sea

def hasTarget(vision):
    return bool(vision.getNumber('tv', 0))

def strafeAlign(drive,vision,visionOffset):

    while True:
        sea.sendLogStates()

        hasTarget = vision.getNumber('tv', "no visionX")
        xOffset = vision.getNumber('tx', "no visionX")
        exponent = 0.8
        if xOffset == "no visionX" or not hasTarget:
            print('no vision')
            yield
            continue
        totalOffset = -xOffset + visionOffset
        exOffset = abs(totalOffset) ** exponent / 20
        if exOffset > .25:
            exOffset = .25
        elif exOffset < -.25:
            exOffset = -.25
        if totalOffset < -0.0:
            drive.drive(-exOffset,0,0)
        elif totalOffset > 0.0:
            drive.drive(exOffset,0,0)
        if abs(totalOffset) <= 2:
            #Original tolerance: 1
            yield True
        else:
            yield False

def driveToTargetDistance(drive, vision):

    help = 0

def waitForVision(vision):
    count = 0
    yield
    while not hasTarget(vision):
        count += 1
        if count > 50:
            return False
        yield
    return True
