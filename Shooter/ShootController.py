__author__ = 'Dawson'
from  .Flywheels import Flywheels
from .Intake import Intake
import wpilib
class ShootController():

    def __init__(self, left, right, intake, switch, switch2):#switch is wpilib.DigitalInput(port)
        self.LeftTalon = left
        self.RightTalon = right
        self.IntakeTalon = intake
        self.Switch = switch
        self.Switch2 = switch2
        self.Flywheels = Flywheels(self.LeftTalon, self.RightTalon)
        self.Intake = Intake(self.IntakeTalon)

    def invertFlywheels(self):
        self.Flywheels.invertFlywheels()

    def update(self, isIntakeButtonPushed, isFlywheelButtonPushed, isShootButtonPushed, isDischargeButtonPushed = False): #This should be always called

        if (isDischargeButtonPushed):
            self.Flywheels.driveSpeed(0)
            self.Intake.dischargeBall()
        else:
            if isIntakeButtonPushed:
                if not (self.Switch.get() == 0 or self.Switch2.get() == 0):
                    # if not isFlywheelButtonPushed:
                    self.Intake.intakeBall()
                else:
                    self.Intake.stop()
            elif isShootButtonPushed:
                if self.Flywheels.readyToShoot():
                    self.Intake.intakeBall()
            else:
                self.Intake.stop()

            if isFlywheelButtonPushed:
                self.Flywheels.driveAuto()
            else:
                self.Flywheels.driveSpeed(0)




