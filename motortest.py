import wpilib
import ctre
import seamonsters as sea

class MotorTestBot(sea.GeneratorBot):

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
        self.joystickLog = sea.LogState("Control")

        self.joy = wpilib.Joystick(0)

    def teleop(self):
        self.statusLog.update("Running!")

        selectedI = 0

        while True:
            yield
            talon = self.talons[selectedI]
            self.updateTalonLog(selectedI, talon)

            if self.joy.getRawButton(1):
                control = -self.joy.getY()
                mode = talon.getControlMode()
                value = None
                if mode == ctre.CANTalon.ControlMode.PercentVbus:
                    value = control
                elif mode == ctre.CANTalon.ControlMode.Voltage:
                    value = control * 12
                self.joystickLog.update(value)
                if value is not None:
                    talon.set(value)
                talon.enable()
            else:
                self.joystickLog.update("Off")
                talon.disable()
            sea.sendLogStates()

            if self.joy.getRawButton(5):
                selectedI += 1
                if selectedI >= len(self.talons):
                    selectedI = len(self.talons) - 1
                self.selectedLog.update(self.talons[selectedI].getDeviceID())
                sea.sendLogStates()
                while self.joy.getRawButton(5):
                    yield
            if self.joy.getRawButton(4):
                selectedI -= 1
                if selectedI < 0:
                    selectedI = 0
                self.selectedLog.update(self.talons[selectedI].getDeviceID())
                sea.sendLogStates()
                while self.joy.getRawButton(4):
                    yield

            if self.joy.getRawButton(9):
                talon.setControlMode((talon.getControlMode() + 1) % 8)
                self.updateTalonLog(selectedI, talon)
                sea.sendLogStates()
                while self.joy.getRawButton(9):
                    yield
            if self.joy.getRawButton(8):
                mode = talon.getControlMode() - 1
                if mode < 0:
                    mode = 7
                talon.setControlMode(mode)
                self.updateTalonLog(selectedI, talon)
                sea.sendLogStates()
                while self.joy.getRawButton(8):
                    yield

    def updateTalonLog(self, i, talon):
        self.selectedLog.update(talon.getDeviceID())
        self.modeLog.update(sea.talonModeToString(talon.getControlMode()))
        self.outputVoltageLog.update(talon.getOutputVoltage())
        self.outputCurrentLog.update(talon.getOutputCurrent())
        self.encoderPositionLog.update(talon.getPosition())
        self.encoderSpeedLog.update(talon.getSpeed())
        self.pidLog.update(
            str(talon.getP()) + "," + str(talon.getI()) + ","
            + str(talon.getD()) + "," + str(talon.getF()))

if __name__ == "__main__":
    wpilib.run(MotorTestBot)
