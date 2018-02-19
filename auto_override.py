import seamonsters as sea
import wpilib

def override():
    sL = wpilib.DriverStation.getInstance().getLocation()
    if sea.getSwitch("Start_Location_1",False):
        locate = 1
    elif not sea.getSwitch("Start_Location_2",False):
        locate = 2
    elif not sea.getSwitch("Starting_Location_3",False):
        locate = 3

    if sL != locate:
        sL = locate
    return sL
