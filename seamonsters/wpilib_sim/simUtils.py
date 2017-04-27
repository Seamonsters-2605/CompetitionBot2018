__author__ = "jacobvanthoog"

import wpilib
import ctre
import time
import hal
import math


class Joystick:
    
    # Some of this was copied from robotpy:
    # http://robotpy.readthedocs.io/en/latest/_modules/wpilib/joystick.html
    
    kDefaultXAxis = 0
    kDefaultYAxis = 1
    kDefaultZAxis = 2
    kDefaultTwistAxis = 2
    kDefaultThrottleAxis = 3
    kDefaultTriggerButton = 1
    kDefaultTopButton = 2
    
    class AxisType:
        kX = 0
        kY = 1
        kZ = 2
        kTwist = 3
        kThrottle = 4
        kNumAxis = 5
    
    class ButtonType:
        kTrigger = 0
        kTop = 1
        kNumButton = 2
    
    class RumbleType:
        kLeftRumble_val = 0
        kRightRumble_val = 1
        
    def __init__(self, port, numAxisTypes=None, numButtonTypes=None):
        self.port = port
        self._log("Init")
        
        if numAxisTypes is None:
            self.axes = [0]*self.AxisType.kNumAxis
            self.axes[self.AxisType.kX] = self.kDefaultXAxis
            self.axes[self.AxisType.kY] = self.kDefaultYAxis
            self.axes[self.AxisType.kZ] = self.kDefaultZAxis
            self.axes[self.AxisType.kTwist] = self.kDefaultTwistAxis
            self.axes[self.AxisType.kThrottle] = self.kDefaultThrottleAxis
        else:
            self.axes = [0]*numAxisTypes

        if numButtonTypes is None:
            self.buttons = [0]*self.ButtonType.kNumButton
            self.buttons[self.ButtonType.kTrigger] = self.kDefaultTriggerButton
            self.buttons[self.ButtonType.kTop] = self.kDefaultTopButton
        else:
            self.buttons = [0]*numButtonTypes

        self.outputs = 0
        self.leftRumble = 0
        self.rightRumble = 0
    
    def _log(self, *args):
        print("Joystick", str(self.port) + ": ", end = "")
        print(*args)
    
    def getX(self, hand=None):
        return self.getRawAxis(self.axes[self.AxisType.kX])
    
    def getY(self, hand=None):
        return self.getRawAxis(self.axes[self.AxisType.kY])
    
    def getZ(self, hand=None):
        return self.getRawAxis(self.axes[self.AxisType.kZ])
    
    def getTwist(self):
        return self.getRawAxis(self.axes[self.AxisType.kTwist])
    
    def getThrottle(self):
        return self.getRawAxis(self.axes[self.AxisType.kThrottle])
    
    def getRawAxis(self, axis):
        return 0.0
    
    def getAxis(self, axis):
        if axis == self.AxisType.kX:
            return self.getX()
        elif axis == self.AxisType.kY:
            return self.getY()
        elif axis == self.AxisType.kZ:
            return self.getZ()
        elif axis == self.AxisType.kTwist:
            return self.getTwist()
        elif axis == self.AxisType.kThrottle:
            return self.getThrottle()
        else:
            raise ValueError("Invalid axis specified! Must be one of wpilib.Joystick.AxisType, or use getRawAxis instead")
    
    def getAxisCount(self):
        return self.AxisType.kNumAxis
    
    def getTrigger(self, hand=None):
        return self.getRawButton(self.buttons[self.ButtonType.kTrigger])
    
    def getTop(self, hand=None):
        return self.getRawButton(self.buttons[self.ButtonType.kTop])
    
    def getBumper(self, hand=None):
        return False
    
    def getRawButton(self, button):
        return False
    
    def getButtonCount(self):
        return self.ButtonType.kNumButton
    
    def getPOV(self, pov=0):
        return -1.0
    
    def getPOVCount(self):
        return 1
    
    def getButton(self, button):
        if button == self.ButtonType.kTrigger:
            return self.getTrigger()
        elif button == self.ButtonType.kTop:
            return self.getTop()
        else:
            raise ValueError("Invalid button specified! Must be one of wpilib.Joystick.ButtonType, or use getRawButton instead")
    
    def getMagnitude(self):
        return math.sqrt(math.pow(self.getX(), 2) + math.pow(self.getY(), 2))
    
    def getDirectionRadians(self):
        return math.atan2(self.getX(), -self.getY())
    
    def getDirectionDegrees(self):
        return math.degrees(self.getDirectionRadians())
    
    def getAxisChannel(self, axis):
        return self.axes[axis]
    
    def setAxisChannel(self, axis, channel):
        self.axes[axis] = channel
    
    def getIsXbox(self):
        return False
    
    def getType(self):
        return 0 # what should this be? (should be an integer)
    
    def getName(self):
        return "nonexistent joystick"
    
    def setRumble(self, type, value):
        self._log("Rumble " + type + " " + value)
    
    def setOutput(self, outputNumber, value):
        self.outputs = (self.outputs & ~(value << (outputNumber-1))) | (value << (outputNumber-1))
        self.flush_outputs()
    
    def setOutputs(self, value):
        self.outputs = value
        self.flush_outputs()
    
    def flush_outputs(self):
        self._log("Flush outputs", self.outputs)



class CANTalon:
    
    # Classes taken from robotpy:
    # http://robotpy.readthedocs.io/en/latest/_modules/wpilib/cantalon.html

    # TODO: Update this for 2017!
    
    class ControlMode:
        PercentVbus = 0
        Position = 1
        Speed = 2
        Current = 3
        Voltage = 4
        Follower = 5
        MotionProfile = 6
        Disabled = 7
        
    class FeedbackDevice:
        QuadEncoder = 0
        AnalogPot = 1
        AnalogEncoder = 2
        EncRising = 3
        EncFalling = 4
        CtreMagEncoder_Relative = 5
        CtreMagEncoder_Absolute = 6
        PulseWidth = 7
        
    class FeedbackDeviceStatus:
        Unknown = 0
        Present = 1
        NotPresent = 2
        
    class PIDSourceType:
        kDisplacement = 0
        kRate = 1
        
    class SetValueMotionProfile:
        Disable = 0
        Enable = 1
        Hold = 2
        
    class StatusFrameRate:
        General = 0
        Feedback = 1
        QuadEncoder = 2
        AnalogTempVbat = 3
        PulseWidth = 4
        
    class TrajectoryPoint:
        position = 0
        velocity = 0
        timeDurMs = 0
        profileSlotSelect = 0
        velocityOnly = False
        isLastPoint = False
        zeroPos = False
        
    
    
    def __init__(self, port, controlPeriodMs=None, enablePeriodMs=None):
        self.port = port
        self._log("Init")
        self.values = [0 for i in range(0, 16)]
        self.lastPositionValue = 0
        self.controlMode = ctre.CANTalon.ControlMode.PercentVbus
        self.controlEnabled = True
        self.inverted = False
        
        self.p = 1.0
        self.i = 0.0
        self.d = 1.0
        self.f = 0.0
        
        self.maxChangePerTick = 400.0
        
        updateFunctions.append(self._update)
        cantalons.append(self)
        pass
    
    def _update(self):
        value = self.values[self.controlMode]
        updatePosition = False
        if self.controlMode == CANTalon.ControlMode.Current:
            pass
        elif self.controlMode == CANTalon.ControlMode.Disabled:
            pass
        elif self.controlMode == CANTalon.ControlMode.Follower:
            pass
        elif self.controlMode == CANTalon.ControlMode.MotionProfile:
            pass
        
        elif self.controlMode == CANTalon.ControlMode.PercentVbus:
            self.values[CANTalon.ControlMode.Voltage] = value * 12.0
            self.values[CANTalon.ControlMode.Speed] = \
                value * self.maxChangePerTick * 5.0
            updatePosition = True
                
        elif self.controlMode == CANTalon.ControlMode.Position:
            diff = value - self.lastPositionValue
            self.values[CANTalon.ControlMode.PercentVbus] = \
                diff / self.maxChangePerTick
            self.values[CANTalon.ControlMode.Voltage] = \
                diff / self.maxChangePerTick * 12.0
            self.values[CANTalon.ControlMode.Speed] = diff * 5.0
            self.lastPositionValue = value
            updatePosition = True
            
        elif self.controlMode == CANTalon.ControlMode.Speed:
            self.values[CANTalon.ControlMode.PercentVbus] = \
                value / self.maxChangePerTick / 5.0
            self.values[CANTalon.ControlMode.Voltage] = \
                value * 12.0 / self.maxChangePerTick / 5.0
            updatePosition = True
                
        elif self.controlMode == CANTalon.ControlMode.Voltage:
            self.values[CANTalon.ControlMode.PercentVbus] = value / 12.0
            self.values[CANTalon.ControlMode.Speed] = \
                value / 12.0 * self.maxChangePerTick * 5.0
            updatePosition = True
        
        if updatePosition:
            self.values[CANTalon.ControlMode.Position] += \
                self.values[CANTalon.ControlMode.Speed] / 5.0
            
    
    def _log(self, *args):
        print("CANTalon", str(self.port) + ": ", end = "")
        print(*args)
    
    def getDescription(self):
        return "CANTalon ID " + str(self.port)
    
    def changeControlMode(self, controlMode):
        self._log("Change control mode:", controlMode)
        self.controlMode = controlMode
        if controlMode == CANTalon.ControlMode.Disabled:
            self.controlEnabled = False
        
    def setControlMode(self, controlMode):
        self.changeControlMode(controlMode)
        
    def getControlMode(self):
        return self.controlMode
        
    def disableControl(self):
        self._log("Disable control")
        self.controlEnabled = False
        
    def enableControl(self):
        self._log("Enable control")
        self.controlEnabled = True
        
    def isControlEnabled(self):
        return self.controlEnabled
        
    def disable(self):
        self.disableControl()
        
    def enable(self):
        self.enableControl()
        
    def isEnabled(self):
        return self.isControlEnabled()
        
    def get(self):
        return self.values[self.controlMode]
        
    def getSetpoint(self):
        return self.get()
        
    def getOutputCurrent(self):
        return self.values[ctre.CANTalon.ControlMode.Current]
        
    def getOutputVoltage(self):
        return self.values[ctre.CANTalon.ControlMode.Voltage]
        
    def getPosition(self):
        return self.values[ctre.CANTalon.ControlMode.Position]
        
    def getEncPosition(self):
        return self.getPosition()
        
    def getSpeed(self):
        return self.values[ctre.CANTalon.ControlMode.Speed]
        
    def getEncVelocity(self):
        return self.getSpeed()
        
    def getError(self):
        return 0.0
        
    def getClosedLoopError(self):
        return 0.0
        
    def set(self, outputValue, syncGroup=0):
        self._log("Set:", outputValue)
        self.values[self.controlMode] = outputValue
        
    def setSetpoint(self, setpoint):
        self.set(setpoint)
        
    def setPID(self, p, i, d, f):
        self._log("Set PID:", p, i, d, f)
        self.p = p
        self.i = i
        self.d = d
        self.f = f
        
    def getP(self):
        return self.p
        
    def getI(self):
        return self.i
        
    def getD(self):
        return self.d
        
    def getF(self):
        return self.f
        
    def setInverted(self, isInverted):
        self._log("Set inverted", isInverted)
        self.inverted = isInverted
        
    def getInverted(self):
        return self.inverted
        
    def setFeedbackDevice(self, device):
        self._log("Set feedback device:", device)
        
    def stopMotor(self):
        self._log("Stop")
        
    def reset(self):
        self._log("Reset")
        
    def reverseOutput(self, flip):
        self._log("Reverse output", flip)
        
    def reverseSensor(self, flip):
        self._log("Reverse sensor", flip)
        
        
updateFunctions = [ ]
cantalons = [ ]

def addUpdateFunction(function):
    updateFunctions.append(function)

def getUpdateFunctions():
    return updateFunctions

def getCANTalons():
    return cantalons
        

# loop at 50 Hz
def robotLoop(function):
    lastTime = time.time()
    
    try:
        while True:
            function()
            for f in updateFunctions:
                f()
            
            while time.time() - lastTime < 1.0 / 50.0:
                pass
        
            lastTime = time.time()
    except KeyboardInterrupt:
        print("\nQuitting")
        return

def replaceWpilib():
    ctre.CANTalon = CANTalon
    wpilib.Joystick = Joystick
