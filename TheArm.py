__author__ = "jacobvanthoog"

import wpilib, math
from Arm.ArmReplay import ArmReplay
from Arm.ArmReplayReader import ArmReplayReader
from JoystickLib.Gamepad import Gamepad

class Arm:
    # use JoystickLib.Gamepad!
    def __init__(self, gamepad):
        self.Gamepad = gamepad
        self.Arm1 = wpilib.CANTalon(6)
        self.Arm1.reverseSensor(True)
        self.Arm2 = wpilib.CANTalon(7)
        self.Arm2.reverseSensor(True)
        self.Control = ArmReplay(self.Arm1, self.Arm2)
        self.Replay = None
        self.LastPathName = ""
        self.ControlEnabled = True

    def update(self):
        if self.Gamepad.getRawButton(Gamepad.LJ):
            print("Arm emergency stop!")
            self.Replay.disable()
            self.Arm1.disable()
            self.Arm2.disable()
            self.Replay = None
            self.ControlEnabled = False

        if not self.ControlEnabled:
            return
        
        self.Control.update()
        if self.Gamepad.getRawButton(Gamepad.LB):
            if self.Replay is not None:
                self.Replay.update()
            else:
                print("No path loaded!")
        if self.Gamepad.getRawButton(Gamepad.START):
            print("Arm path reset")
            if self.Replay is not None:
                self.Replay.disable()
                self.Replay = None
        pov = self.Gamepad.getPOV()
        if not pov == -1:
            pov = round(pov / 90)
            if pov == 0 or pov == 4: # could round up
                self.loadReplay("1")
            elif pov == 1:
                self.loadReplay("2")
            elif pov == 2:
                self.loadReplay("3")
            elif pov == 3:
                self.loadReplay("4")

        if self.Gamepad.getRawButton(Gamepad.BACK):
            if self.LastPathName == "":
                print("No path loaded!")
            else:
                print("Return path for", self.LastPathName)
                last = self.LastPathName
                self.loadReplay(self.LastPathName + "a")
                self.LastPathName = last
        
    def loadReplay(self, name):
        if self.Replay is not None:
            self.Replay.disable()
        try:
            self.Replay = ArmReplayReader(self.Control, name)
        except Exception as e:
            print("Error while loading path")
            print(e)
            return
        self.Replay.enable()
        self.LastPathName = name
        print("Arm path", name, "is loaded and ready")
