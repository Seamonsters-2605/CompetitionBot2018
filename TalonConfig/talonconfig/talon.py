_author_ = "WZ"
import wpilib
class TalonConfigure:
        def __init__(self, talon):
            pass
        def setDriveTalonVoltage(self, talon):
            talon.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
            talon.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
            talon.setPID(wpilib.CANTalon.setPID(.5,0,2,0))
        def setDriveTalonSpeed(self, talon):
            talon.setPID(wpilib.CANTalon.setPID(.5,0,2,0))
            talon.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
            talon.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        def intakeTalonSpeed(self, talon):
            talon.setDriveTalonSpeed(talon)
        def intakeTalonSpeed(self, talon):
            talon.setDriveTalonVoltage(talon)
        def intakeTalonPos(self, talon):
            talon.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
            talon.setPID(wpilib.CANTalon.setPID(0.5,0,2,0))
            talon.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        def flywheelSpeed(self, talon):
            talon.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
            talon.setPID(wpilib.CANTalon.setPID(.5, .001, 2, 0))
            talon.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        def flywheelVoltage(self, talon):
            talon.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
            talon.setPID(wpilib.CANTalon.setPID(.5, .001, 2, 0))
            talon.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)

