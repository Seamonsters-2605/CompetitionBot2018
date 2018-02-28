import seamonsters as sea
import wpilib


def override():
    sL = wpilib.DriverStation.getInstance().getLocation()
    if sea.getSwitch('Loc1',defaultValue=False):
        locate = 1
    elif sea.getSwitch("Loc2",defaultValue=False):
        locate = 2
    elif sea.getSwitch("Loc3",defaultValue=False):
        locate = 3
    elif sea.getSwitch("None",defaultValue=False):
        locate = sL


    if sL != locate:
        sL = locate
    return sL