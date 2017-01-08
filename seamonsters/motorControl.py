__author__ = 'jacobvanthoog'
import wpilib
from seamonsters.drive import DriveInterface

class MotorManager:
    """
    A motor manager manages many CANTalons, with associated MultiMode's. The
    MultiMode can be in voltage, speed, or jeff/position mode. The drive mode
    and maximum velocity of all can be set at once.
    """
    def __init__(self):
        self.talons = [ ]
        self.driveMode = DriveInterface.DriveMode.VOLTAGE
        self.multiModes = [ ]
        self.voltageModes = [ ]
        self.speedModes = [ ]
        self.jeffModes = [ ]
        
        self.maxSpeed = 400
    
    def addMotor(self, talon, inverted=False):
        """
        Adds a CANTalon to the manager. Creates a corresponding MultiMode, set
        to the current max velocity, drive mode, and specified invert setting.
        This MultiMode is returned.
        """
        self.talons.append(talon)
        
        voltage = VoltageMode(talon)
        voltage.invert(inverted)
        self.voltageModes.append(voltage)
        
        speed = SpeedMode(talon)
        speed.invert(inverted)
        speed.setMaxSpeed(self.maxSpeed)
        self.speedModes.append(speed)
        
        jeff = JeffMode(talon)
        jeff.invert(inverted)
        jeff.setMaxSpeed(self.maxSpeed)
        self.jeffModes.append(jeff)
        
        initial = None
        
        if self.driveMode == DriveInterface.DriveMode.VOLTAGE:
            initial = voltage
        if self.driveMode == DriveInterface.DriveMode.SPEED:
            initial = speed
        if self.driveMode == DriveInterface.DriveMode.POSITION:
            initial = jeff
        multi = MultiMode(talon, initial)
        self.multiModes.append(multi)
        
        return multi
        
    def setDriveMode(self, mode):
        """
        Set the drive mode of all MultiMode's, using constants from
        seamonsters.drive.DriveInterface.DriveMode. Default is VOLTAGE.
        """
        self.driveMode = mode
        i = 0
        for m in self.multiModes:
            if self.driveMode == DriveInterface.DriveMode.VOLTAGE:
                m.setSpeedControl(self.voltageModes[i])
            if self.driveMode == DriveInterface.DriveMode.SPEED:
                m.setSpeedControl(self.speedModes[i])
            if self.driveMode == DriveInterface.DriveMode.POSITION:
                m.setSpeedControl(self.jeffModes[i])
            i += 1
            
    def getDriveMode(self, mode):
        """
        Get the drive mode that was last set.
        """
        return self.driveMode
        
    def setMaxSpeed(self, speed):
        """
        Set the maximum speed of SpeedModes and JeffModes.
        """
        self.maxSpeed = speed
        
        for m in self.speedModes:
            m.setMaxSpeed(speed)
            
        for m in self.jeffModes:
            m.setMaxSpeed(speed)
    
    def getMaxSpeed(self):
        """
        Get the last set max speed.
        """
        return self.maxSpeed

class MotorSpeedControl:
    """
    An abstract interface for controlling the speed of a motor. Keeps track of
    and controls a singe CANTalon.
    """
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
    """
    An implementation of MotorSpeedControl that wraps another MotorSpeedControl
    implementation. All interface calls go to that object. This allows switching
    out the underlying MotorSpeedControl. Implementation.
    """
    def __init__(self, talon, speedControl):
        """
        Initialize with a talon and initial MotorSpeedControl. The zero() method
        of speedControl will be called.
        """
        self.talon = talon
        self.speedControl = speedControl
        self.speedControl.zero()
        
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
        """
        Set the current MotorSpeedControl implementation. The zero() method
        will be called.
        """
        if self.speedControl != speedControl:
            self.speedControl = speedControl
            speedControl.zero()
        
    def getSpeedControl(self):
        """
        Set the current MotorSpeedControl implementation.
        """
        return self.speedControl

class VoltageMode(MotorSpeedControl):
    """
    A CANTalon in voltage mode (actually PercentVbus).
    """
    def __init__(self, talon):
        self.talon = talon
        self.zero()
        self.inverted = 1 # can be 1 or -1
        self.speed = 0
        
    def zero(self):
        if not (self.talon.getControlMode() == \
                wpilib.CANTalon.ControlMode.PercentVbus):
            self.talon.changeControlMode(
                wpilib.CANTalon.ControlMode.PercentVbus)
        
    def set(self, speed):
        self.speed = speed * self.inverted
    
    def update(self):
        self.talon.set(self.speed)
    
    def invert(self, enabled=True):
        """
        Choose whether to invert the direction of the motor.
        """
        self.inverted = -1 if enabled else 1


class SpeedMode(MotorSpeedControl):
    """
    A CANTalon in speed mode.
    """
    def __init__(self, talon):
        self.talon = talon
        self.zero()
        self.inverted = 1 # can be 1 or -1
        self.speed = 0
        self.maxSpeed = 2000
        
    def zero(self):
        if not (self.talon.getControlMode() == \
                wpilib.CANTalon.ControlMode.Speed):
            self.talon.changeControlMode(
                wpilib.CANTalon.ControlMode.Speed)
        
    def set(self, speed):
        self.speed = speed * self.inverted * self.maxSpeed
    
    def update(self):
        self.talon.set(self.speed)
    
    def invert(self, enabled=True):
        """
        Choose whether to invert the direction of the motor.
        """
        self.inverted = -1 if enabled else 1
        
    def setMaxSpeed(self, speed):
        """
        Set the maximum speed of the motor in encoder ticks per 1/50th of a
        second. The value passed to the CANTalon will be this value multiplied
        by 5, because the CANTalon uses units of encoder ticks per 1/10th of a
        second.
        """
        self.maxSpeed = speed * 5
    
    def getMaxSpeed(self):
        """
        Get the maximum speed of the motor in encoder ticks per 1/50th of a
        second.
        """
        return self.maxSpeed / 5

class JeffMode(MotorSpeedControl):

    """
    "Jeff Mode" is incremental position mode -- it constantly increments the
    position of the motors to mock speed mode.
    """
    
    def __init__(self, talon):
        """
        Initialize JeffMode with a CANTalon. This will automatically zero
        everything and change the control mode -- be careful not to change that
        later on.
        """
        self.talon = talon
        
        self.zero()
        self.inverted = 1 # can be 1 or -1
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
        self.speed = speed * self.inverted * self.maxSpeed
        
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
        self.inverted = -1 if enabled else 1

    def setMaxSpeed(self, speed):
        """
        Set the maximum speed of the motor in encoder ticks per 1/50th of a
        second.
        """
        self.maxSpeed = speed
        
    def getMaxSpeed(self):
        """
        Get the maximum speed of the motor in encoder ticks per 1/50th of a
        second.
        """
        return self.maxSpeed
