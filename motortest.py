import wpilib
import ctre
import seamonsters as sea
from networktables import NetworkTables

class MotorTestBot(sea.GeneratorBot):

    def robotInit(self):
        self.talons = [ctre.WPI_TalonSRX(i) for i in range(1,8)]
        for talon in self.talons:
            talon.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, 0)

        self.statusLog = sea.LogState("!Motor Tester!")
        self.selectedLog = sea.LogState("Selected Motor")
        self.modeLog = sea.LogState("Motor Control Mode")
        self.outputVoltageLog = sea.LogState("Output Voltage")
        self.outputCurrentLog = sea.LogState("Output Current")
        self.encoderPositionLog = sea.LogState("Encoder Position")
        self.encoderSpeedLog = sea.LogState("Encoder Speed")
        self.pidLog = sea.LogState("PIDF")
        self.setLog = sea.LogState("Set")

        self.joy = wpilib.Joystick(0)

        self.commandReader = sea.DashboardCommandReader()

    def teleop(self):
        self.statusLog.update("Running!")

        self.selectedI = 0
        self.commandReader.reset()
        self.setValue = 0

        while True:
            yield
            talon = self.talons[self.selectedI]
            self.updateTalonLog()

            if self.joy.getRawButton(1):
                while self.joy.getRawButton(1):
                    self.setValue = \
                        -self.joy.getY() * (self.joy.getTwist() + 1) / 2
                    talon.set(ctre.ControlMode.PercentOutput, self.setValue)
                    self.updateTalonLog()
                    yield
                self.setValue = None
                talon.disable()

            if self.joy.getRawButton(5):
                self.selectedI += 1
                if self.selectedI >= len(self.talons):
                    self.selectedI = len(self.talons) - 1
                yield from self.buttonHeld(5)
            if self.joy.getRawButton(4):
                self.selectedI -= 1
                if self.selectedI < 0:
                    self.selectedI = 0
                yield from self.buttonHeld(4)

    def buttonHeld(self, buttonNum):
        while self.joy.getRawButton(buttonNum):
            self.updateTalonLog()
            yield

    def updateTalonLog(self):
        talon = self.talons[self.selectedI]
        self.selectedLog.update(talon.getDeviceID())
        self.modeLog.update(sea.talonModeToString(talon.getControlMode()))
        self.outputVoltageLog.update(talon.getMotorOutputVoltage())
        self.outputCurrentLog.update(talon.getOutputCurrent())
        self.encoderPositionLog.update(talon.getSelectedSensorPosition(0))
        self.encoderSpeedLog.update(talon.getSelectedSensorVelocity(0))

        pidf = (talon.configGetParameter(
                    ctre.WPI_TalonSRX.ParamEnum.eProfileParamSlot_P, 0, 0),
                talon.configGetParameter(
                    ctre.WPI_TalonSRX.ParamEnum.eProfileParamSlot_I, 0, 0),
                talon.configGetParameter(
                    ctre.WPI_TalonSRX.ParamEnum.eProfileParamSlot_D, 0, 0),
                talon.configGetParameter(
                    ctre.WPI_TalonSRX.ParamEnum.eProfileParamSlot_F, 0, 0))
        pidfStr = ""
        for i in range(0, 4):
            pidfStr += str(pidf[i])
            if i != 3:
                pidfStr += ","
        self.pidLog.update(pidfStr)

        self.setLog.update(self.setValue)
        sea.sendLogStates()

if __name__ == "__main__":
    wpilib.run(MotorTestBot)
