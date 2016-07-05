__author__ = "jacobvanthoog"

import wpilib
import time
import hal

class CANTalon:
    
    # Classes taken from robotpy:
    # http://robotpy.readthedocs.io/en/latest/_modules/wpilib/cantalon.html
    
    class ControlMode:
        PercentVbus = hal.TalonSRXConst.kMode_DutyCycle
        Position = hal.TalonSRXConst.kMode_PositionCloseLoop
        Speed = hal.TalonSRXConst.kMode_VelocityCloseLoop
        Current = hal.TalonSRXConst.kMode_CurrentCloseLoop
        Voltage = hal.TalonSRXConst.kMode_VoltCompen
        Follower = hal.TalonSRXConst.kMode_SlaveFollower
        MotionProfile = hal.TalonSRXConst.kMode_MotionProfile
        Disabled = hal.TalonSRXConst.kMode_NoDrive
        
    class FeedbackDevice:
        QuadEncoder = hal.TalonSRXConst.kFeedbackDev_DigitalQuadEnc
        AnalogPot = hal.TalonSRXConst.kFeedbackDev_AnalogPot
        AnalogEncoder = hal.TalonSRXConst.kFeedbackDev_AnalogEncoder
        EncRising = hal.TalonSRXConst.kFeedbackDev_CountEveryRisingEdge
        EncFalling = hal.TalonSRXConst.kFeedbackDev_CountEveryFallingEdge
        CtreMagEncoder_Relative = hal.TalonSRXConst.kFeedbackDev_CtreMagEncoder_Relative
        CtreMagEncoder_Absolute = hal.TalonSRXConst.kFeedbackDev_CtreMagEncoder_Absolute
        PulseWidth = hal.TalonSRXConst.kFeedbackDev_PosIsPulseWidth
        
    class FeedbackDeviceStatus:
        Unknown = hal.TalonSRXConst.kFeedbackDevStatus_Unknown
        Present = hal.TalonSRXConst.kFeedbackDevStatus_Present
        NotPresent = hal.TalonSRXConst.kFeedbackDevStatus_NotPresent
        
    class PIDSourceType:
        kDisplacement = 0
        kRate = 1
        
    class SetValueMotionProfile:
        Disable = hal.TalonSRXConst.kMotionProfile_Disable
        Enable = hal.TalonSRXConst.kMotionProfile_Enable
        Hold = hal.TalonSRXConst.kMotionProfile_Hold
        
    class StatusFrameRate:
        General = hal.TalonSRXConst.kStatusFrame_General
        Feedback = hal.TalonSRXConst.kStatusFrame_Feedback
        QuadEncoder = hal.TalonSRXConst.kStatusFrame_Encoder
        AnalogTempVbat = hal.TalonSRXConst.kStatusFrame_AnalogTempVbat
        PulseWidth = hal.TalonSRXConst.kStatusFrame_PulseWidth
        
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
        self.controlMode = wpilib.CANTalon.ControlMode.PercentVbus
        self.controlEnabled = True
        self.inverted = False
        
        self.p = 1.0
        self.i = 0.0
        self.d = 1.0
        self.f = 0.0
        
        self.maxChangePerTick = 400.0
        
        updateFunctions.append(self._update)
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
        return self.values[wpilib.CANTalon.ControlMode.Current]
        
    def getOutputVoltage(self):
        return self.values[wpilib.CANTalon.ControlMode.Voltage]
        
    def getPosition(self):
        return self.values[wpilib.CANTalon.ControlMode.Position]
        
    def getEncPosition(self):
        return self.getPosition()
        
    def getSpeed(self):
        return self.values[wpilib.CANTalon.ControlMode.Speed]
        
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
    wpilib.CANTalon = CANTalon
