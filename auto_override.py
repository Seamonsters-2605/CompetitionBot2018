import seamonsters as sea
import wpilib


def override():
    sL = wpilib.DriverStation.getInstance().getLocation()
    if sea.getSwitch('Loc1',False):
        locate = 1
    elif not sea.getSwitch("Loc2",False):
        locate = 2
    elif not sea.getSwitch("Loc3",False):
        locate = 3
    elif not sea.getSwitch("None",False):
        locate = sL


    if sL != locate:
        sL = locate
    return sL