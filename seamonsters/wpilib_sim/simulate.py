__author__ = "jacobvanthoog"

import wpilib
import sys
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
    
    def __init__(self, port):
        self.port = port
        self._log("Init")
        self.values = [0 for i in range(0, 16)]
        self.controlMode = wpilib.CANTalon.ControlMode.PercentVbus
        self.controlEnabled = True
        self.enabled = True
        pass
    
    def _log(self, *args):
        print("CANTalon", str(self.port) + ": ", end = "")
        print(*args)
    
    def changeControlMode(self, controlMode):
        self._log("Change control mode:", controlMode)
        self.controlMode = controlMode
        
    def getControlMode(self):
        return self.controlMode
        
    def disableControl(self):
        self._log("Disable control")
        self.controlEnabled = False
        
    def enableControl(self):
        self._log("Enable control")
        self.controlEnabled = True
        
    def isControlEnabled(self):
        return self.isControlEnabled
        
    def disable(self):
        self._log("Disable")
        self.enabled = False
        
    def enable(self):
        self._log("Enable")
        self.enabled = True
        
    def isEnabled(self):
        return self.enabled
        
    def get(self):
        return self.values[self.controlMode]
        
    def getPosition(self):
        return self.values[wpilib.CANTalon.ControlMode.Position]
        
    def getEncPosition(self):
        return self.getPosition()
        
    def getSpeed(self):
        return self.values[wpilib.CANTalon.ControlMode.Speed]
        
    def getEncVelocity(self):
        return self.getSpeed()
        
    def set(self, value):
        self._log("Set:", value)
        self.values[self.controlMode] = value
        
    def setPID(self, p, i, d, f):
        self._log("Set PID:", p, i, d, f)
        
    def setFeedbackDevice(self, device):
        self._log("Set feedback device:", device)
        
    def stopMotor(self):
        self._log("Stop")
        

# loop at 50 Hz
def robotLoop(function):
    lastTime = time.time()
    
    while True:
        function()
        
        try:
            while time.time() - lastTime < 1.0 / 50.0:
                pass
        except KeyboardInterrupt:
            print("Quitting")
            return
        lastTime = time.time()

        
def run(robotClass):
    print("Simulating robot:", robotClass)
    
    print("Create robot")
    robot = robotClass()
    
    print("Robot init")
    robot.robotInit()
    
    if len(sys.argv) < 2:
        return
    
    command = sys.argv[1]
    if command == "d":
        print("Disabled init")
        robot.disabledInit()
        print("Disabled periodic")
        robotLoop(robot.disabledPeriodic)
        
    elif command == "a":
        print("Autonomous init")
        robot.autonomousInit()
        print("Autonomous periodic")
        robotLoop(robot.autonomousPeriodic)
        
    elif command == "t":
        print("Teleop init")
        robot.teleopInit()
        print("Teleop periodic")
        robotLoop(robot.teleopPeriodic)
        
    elif command == "s":
        print("Test init")
        robot.testInit()
        print("Test periodic")
        robotLoop(robot.testPeriodic)

print("Simulate!")
wpilib.CANTalon = CANTalon
wpilib.run = run

