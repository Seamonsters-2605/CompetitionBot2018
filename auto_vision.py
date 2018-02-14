import seamonsters as sea

def checkForVisionTarget(vision):
    while True:
        hasTarget = vision.getNumber('tv', 0)
        yield bool(hasTarget)

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
        totalOffset = xOffset - visionOffset
        exOffset = abs(totalOffset) ** exponent / 13.9
        if totalOffset < -0.0:
            drive.drive(-exOffset,0,0)
        elif totalOffset > 0.0:
            drive.drive(exOffset,0,0)
        if abs(totalOffset) <= 0.5:
            #Original tolerance: 1
            yield True
        else:
            yield False

def driveToTargetDistance(drive, vision):

    help = 0
