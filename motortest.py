import wpilib
import ctre
import seamonsters as sea
from networktables import NetworkTables

class MotorTestBot(sea.GeneratorBot):

    VALUE = 4
    P = 0
    I = 1
    D = 2
    F = 3
    NUM_PARAMETERS = 5

    def robotInit(self):
        self.talons = [ctre.CANTalon(i) for i in range(0,8)]
        for talon in self.talons:
            talon.setFeedbackDevice(ctre.CANTalon.FeedbackDevice.QuadEncoder)

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
        self.selectedParameter = MotorTestBot.VALUE
        self.commandReader.reset()
        self.setValue = 0

        enteredValue = False

        while True:
            yield
            talon = self.talons[self.selectedI]
            self.updateTalonLog()

            if not enteredValue:
                self.setValue = None
            if self.joy.getRawButton(1):
                enteredValue = False
                control = -self.joy.getY() * (self.joy.getTwist() + 1) / 2
                mode = talon.getControlMode()
                if mode == ctre.CANTalon.ControlMode.PercentVbus:
                    self.setValue = control
                elif mode == ctre.CANTalon.ControlMode.Position:
                    pass # TODO
                elif mode == ctre.CANTalon.ControlMode.Speed:
                    pass  # TODO
                elif mode == ctre.CANTalon.ControlMode.Current:
                    pass  # TODO
                elif mode == ctre.CANTalon.ControlMode.Voltage:
                    self.setValue = control * 12
            if self.setValue is not None:
                talon.enable()
                talon.set(self.setValue)
            else:
                if not enteredValue:
                    talon.disable()

            sea.sendLogStates()

            if self.joy.getRawButton(5):
                self.selectedI += 1
                if self.selectedI >= len(self.talons):
                    self.selectedI = len(self.talons) - 1
                self.updateTalonLog()
                sea.sendLogStates()
                while self.joy.getRawButton(5):
                    yield
            if self.joy.getRawButton(4):
                self.selectedI -= 1
                if self.selectedI < 0:
                    self.selectedI = 0
                self.updateTalonLog()
                sea.sendLogStates()
                while self.joy.getRawButton(4):
                    yield

            if self.joy.getRawButton(3):
                self.selectedParameter += 1
                if self.selectedParameter >= MotorTestBot.NUM_PARAMETERS:
                    self.selectedParameter = 0
                self.updateTalonLog()
                sea.sendLogStates()
                while self.joy.getRawButton(3):
                    yield
            if self.joy.getRawButton(2):
                self.selectedParameter -= 1
                if self.selectedParameter < 0:
                    self.selectedParameter = MotorTestBot.NUM_PARAMETERS - 1
                self.updateTalonLog()
                sea.sendLogStates()
                while self.joy.getRawButton(2):
                    yield

            if self.joy.getRawButton(9):
                talon.setControlMode((talon.getControlMode() + 1) % 8)
                self.updateTalonLog()
                sea.sendLogStates()
                while self.joy.getRawButton(9):
                    yield
            if self.joy.getRawButton(8):
                mode = talon.getControlMode() - 1
                if mode < 0:
                    mode = 7
                talon.setControlMode(mode)
                self.updateTalonLog()
                sea.sendLogStates()
                while self.joy.getRawButton(8):
                    yield

            command = self.commandReader.getCommand()
            if command is not None:
                value = float(command)
                if self.selectedParameter == MotorTestBot.VALUE:
                    self.setValue = value
                    enteredValue = True
                elif self.selectedParameter == MotorTestBot.P:
                    talon.setP(value)
                elif self.selectedParameter == MotorTestBot.I:
                    talon.setI(value)
                elif self.selectedParameter == MotorTestBot.D:
                    talon.setD(value)
                elif self.selectedParameter == MotorTestBot.F:
                    talon.setF(value)

    def updateTalonLog(self):
        talon = self.talons[self.selectedI]
        self.selectedLog.update(talon.getDeviceID())
        self.modeLog.update(sea.talonModeToString(talon.getControlMode()))
        self.outputVoltageLog.update(talon.getOutputVoltage())
        self.outputCurrentLog.update(talon.getOutputCurrent())
        self.encoderPositionLog.update(talon.getPosition())
        self.encoderSpeedLog.update(talon.getSpeed())

        pidf = (talon.getP(), talon.getI(), talon.getD(), talon.getF())
        pidfStr = ""
        for i in range(0, 4):
            if i == self.selectedParameter:
                pidfStr += "["
            pidfStr += str(pidf[i])
            if i == self.selectedParameter:
                pidfStr += "]"
            if i != 3:
                pidfStr += ","
        self.pidLog.update(pidfStr)

        if self.selectedParameter == MotorTestBot.VALUE:
            self.setLog.update('[' + str(self.setValue) + ']')
        else:
            self.setLog.update(self.setValue)

if __name__ == "__main__":
    wpilib.run(MotorTestBot)
