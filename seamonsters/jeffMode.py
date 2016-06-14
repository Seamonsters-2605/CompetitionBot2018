__author__ = 'jacobvanthoog'
import wpilib

# based off code in HolonomicDrive
class JeffMode:

    """
    "Jeff Mode" is incremental position mode -- it constantly increments the
    position of the motors to mock speed mode. The JeffMode class keeps track
    of and controls a CANTalon.
    """
    
    def __init__(self, talon):
        """
        Initialize JeffMode with a CANTalon. This will automatically zero
        everything and change the control mode -- be careful not to change that
        later on.
        """
        self.Talon = talon

        if not (self.Talon.getControlMode() == wpilib.CANTalon.ControlMode.Position):
            self.Talon.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.zero()
        self.invert = 1 # can be 1 or -1

    def zero(self):
        """
        Zero the encoder target.
        """
        self.encoderTarget = self.Talon.getPosition()

    def set(self, magnitude):
        """
        Rotate the motor at the specified speed (magnitude). This function needs
        to be called in the main loop, 50 times per second for anything useful
        to happen.
        """
        if not abs(self.Talon.getPosition() - self.encoderTarget) \
               > abs(2*magnitude):
            self.encoderTarget += magnitude * self.invert
        self.Talon.set(self.encoderTarget)
    
    def invert(self, enabled=True):
        """
        Choose whether to invert the direction of the motor.
        """
        self.invert = -1 if enabled else 1
