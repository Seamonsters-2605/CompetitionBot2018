__author__ = 'jacobvanthoog'
import wpilib
from seamonsters.drive import DriveInterface

class MotorManager:
    
    def __init__(self):
        self.talons = [ ]
        self.driveMode = DriveInterface.DriveMode.VOLTAGE
        self.multiModes = [ ]
        self.voltageModes = [ ]
        self.speedModes = [ ]
        self.jeffModes [ ]
    
    def addMotor(self, talon):
        

class MotorSpeedControl:
    
    def zero(self):
        """
        This method is implementation specific, and should be called whenever
        you haven't called update() within the past main loop iteration. For
        example, in JeffMode it will zero the encoder targets.
        """
        pass
    
    def set(self, speed):
        """
        Set the speed of the motor, on a scale of -1 to 1.
        """
        pass
    
    def update(self):
        """
        This method is implementation specific, and should be called in the main
        loop, 50 times per second.
        """
        pass


class MultiMode(MotorSpeedControl):
    
    def __init__(self, talon, speedControl):
        self.talon = talon
        self.speedControl = speedControl
        
    def zero(self):
        self.speedControl.zero()
        pass
    
    def set(self, speed):
        self.speedControl.set(speed)
        pass
    
    def update(self):
        self.speedControl.update()
        pass
    
    def setSpeedControl(self, speedControl):
        self.speedControl = speedControl
        speedControl.zero()

class VoltageMode(MotorSpeedControl):
    
    def __init__(self, talon):
        self.talon = talon
        self.zero()
        self.invert = 1 # can be 1 or -1
        self.speed = 0
        
    def zero(self):
        if not (self.talon.getControlMode() == \
                wpilib.CANTalon.ControlMode.PercentVbus):
            self.talon.changeControlMode(
                wpilib.CANTalon.ControlMode.PercentVbus)
        
    def set(self, speed):
        self.speed = speed * self.invert
        pass
    
    def update(self):
        self.talon.set(self.speed)
        pass
    
    def invert(self, enabled=True):
        """
        Choose whether to invert the direction of the motor.
        """
        self.invert = -1 if enabled else 1


class SpeedMode(MotorSpeedControl):
    
    def __init__(self, talon):
        self.talon = talon
        self.zero()
        self.invert = 1 # can be 1 or -1
        self.speed = 0
        self.maxSpeed = 2000
        
    def zero(self):
        if not (self.talon.getControlMode() == \
                wpilib.CANTalon.ControlMode.Speed):
            self.talon.changeControlMode(
                wpilib.CANTalon.ControlMode.Speed)
        
    def set(self, speed):
        self.speed = speed * self.invert * self.maxSpeed
        pass
    
    def update(self):
        self.talon.set(self.speed)
        pass
    
    def invert(self, enabled=True):
        """
        Choose whether to invert the direction of the motor.
        """
        self.invert = -1 if enabled else 1
        
    def setMaxSpeed(self, speed):
        self.maxSpeed = speed * 5


class JeffMode(MotorSpeedControl):

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
        self.talon = talon
        
        self.zero()
        self.invert = 1 # can be 1 or -1
        self.speed = 0
        self.maxSpeed = 400

    def zero(self):
        """
        Zero the encoder target.
        """
        if not (self.talon.getControlMode() == \
                wpilib.CANTalon.ControlMode.Position):
            self.talon.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.encoderTarget = self.talon.getPosition()

    def set(self, speed):
        """
        Set the speed of rotation of the motor. This is the number of rotation
        ticks it moves every time update() is called.
        """
        self.speed = speed * self.invert * self.maxSpeed
        
    def update(self):
        """
        Update the position of the motor. This function needs to be called in
        the main loop, 50 times per second.
        """
        if not abs(self.talon.getPosition() - self.encoderTarget) \
               > abs(2*self.speed):
            self.encoderTarget += self.speed
        self.talon.set(self.encoderTarget)
    
    def invert(self, enabled=True):
        """
        Choose whether to invert the direction of the motor.
        """
        self.invert = -1 if enabled else 1

    def setMaxSpeed(self, speed):
        self.maxSpeed = speed