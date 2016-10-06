__author__ = "jacobvanthoog"

import seamonsters.wpilib_sim.simulate
import math
import wpilib
import sys
import seamonsters
from seamonsters.holonomicDrive import HolonomicDrive
from seamonsters.drive import DriveInterface
from seamonsters.drive import AccelerationFilterDrive
from seamonsters.gamepad import Gamepad
from Shooter import ShootController
import Vision
import networktables
from networktables import NetworkTable

NetworkTable.setServerMode()

num_array = networktables.NumberArray()

# noinspection PyInterpreter,PyInterpreter
class MainRobot (wpilib.IterativeRobot):
    def robotInit(self):

        print("seamonsters-template!")

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.BELT_BROKEN = False
        self.USING_GAMEPAD = True
        self.AUTO_SHOOT_ENABLED = False
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        self.Vision = Vision.Vision()
        self.FL = wpilib.CANTalon(2)
        self.FR = wpilib.CANTalon(1)
        self.BL = wpilib.CANTalon(0)
        self.BR = wpilib.CANTalon(3)
        self.FL.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.FR.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.BL.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.BR.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.FL.setPID(1.0, 0.0, 3.0, 0.0)
        self.FR.setPID(1.0, 0.0, 3.0, 0.0)
        self.BL.setPID(1.0, 0.0, 3.0, 0.0)
        self.BR.setPID(1.0, 0.0, 3.0, 0.0)


        self.MoveGamepad = Gamepad(port = 0)
        self.ShootGamepad = Gamepad(port = 1)

        self.MoveJoy = seamonsters.joystick.JoystickUtils(0)
        self.MoveJoy.invertY()
        self.TurnJoy = seamonsters.joystick.JoystickUtils(1)
        self.TurnJoy.invertY()

        # 4156 ticks per wheel rotation
        # encoder has 100 raw ticks -- with a QuadEncoder that makes 400 ticks
        # the motor gear has 18 teeth and the wheel has 187 teeth
        # 187 / 18 * 400 = 4155.5556 = ~4156
        self.Drive = HolonomicDrive(self.FL, self.FR, self.BL, self.BR, 4156)
        self.Drive.invertDrive(True)
        # TODO: move magic number to constant
        self.Drive.setWheelOffset(math.radians(27)) #angle of wheels
        self.Drive.setDriveMode(DriveInterface.DriveMode.POSITION)
        self.FilterDrive = AccelerationFilterDrive(self.Drive)

        self.LeftFly = wpilib.CANTalon(4)
        self.LeftFly.reverseOutput(True)
        self.LeftFly.reverseSensor(True)
        self.RightFly = wpilib.CANTalon(5)
        self.LimitSwitch = wpilib.DigitalInput(0)
        self.LimitSwitch2 = wpilib.DigitalInput(1)
        self.Intake = wpilib.CANTalon(8)
        self.Shooter = ShootController.ShootController(\
            self.LeftFly, self.RightFly,\
            self.Intake, self.LimitSwitch, self.LimitSwitch2)
        #self.Shooter.invertFlywheels()
        

    def autonomousInit(self):
        self.shoot = False
        self.rev = 0
        self.time = 0
        self.shoot = False
        self.turn = 0
        self.Drive.zeroEncoderTargets()
        self.needed = 0
        self.start = True
        self.FR.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.FL.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.BL.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.BR.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.turn = 0
        self.need = 0

    def autonomousPeriodic(self):
        if not self.BELT_BROKEN:
            self.time += 1
            if self.time < 250:
                self.FL.set(8.5 * 819.2 / 8)
                self.BR.set(-9 * 819.2 / 8)
                self.FR.set(-9 * 819.2 / 8)
                self.BL.set(8.5 * 819.2 / 8)
            elif (self.time > 300 and self.time < 310):
                self.FL.set(0)
                self.BR.set(0)
                self.FR.set(0)
                self.BL.set(0)
            if self.time > 310:
                if not self.Vision.centerX().__len__() == 0:
                    self.need = abs(self.Vision.centerX()[0] - 240)
                    print (self.need)
                    if self.need > 50:
                        self.turn = self.need * .0005
                    else:
                        self.turn = self.need * .0002
                    if abs(self.Vision.centerX()[0] - 240) < 10:
                        self.shoot = True
                    elif self.Vision.centerX()[0] - 240 > 0:
                        self.FilterDrive.drive(0, 0, -self.turn)
                        self.shoot = False
                    elif self.Vision.centerX()[0] - 240 < 0:
                        self.FilterDrive.drive(0, 0, self.turn)
                        self.shoot = False
                    else:
                        self.shoot = False
                if self.time <= 320:
                    self.shoot = False
                
                if self.shoot == True and self.AUTO_SHOOT_ENABLED:
                    self.rev += 1
                    if self.rev < 100:
                        self.Shooter.update(False, True, False, False)
                    else:
                        self.Shooter.update(False, True, True, False)
        
        else: # belt is broken
            #self.FilterDrive.driveSpeedJeffMode(.5,math.pi/2,0)
            pass
    
    # old version of autonomousPeriodic:
    
    # def autonomousPeriodic(self):
    #
    #     self.time += 1
    #     if self.time < 350:
    #         self.start = True
    #     if self.start == True:
    #         self.FilterDrive.drive(1, math.pi/2, 0)
    #     if self.time > 350:
    #         self.start = False
    #         print ("time is at 350")
    #         # self.FilterDrive.drive(0, 0, 0)
    #         if not self.Vision.centerX().__len__() == 0:
    #             print("passed")
    #             self.needed = abs(self.Vision.centerX()[0] - 235)
    #             print (self.needed)
    #             if self.needed > 50:
    #                 self.turn = self.needed * .009
    #             else:
    #                 self.turn = self.needed * .0008
    #
    #             if abs(self.Vision.centerX()[0] - 235) < 10:
    #                 self.shoot = True
    #                 print ("Alligned")
    #             elif self.Vision.centerX()[0] - 235 > 0:
    #                 self.shoot = False
    #             elif self.Vision.centerX()[0] - 235 < 0:
    #                 self.shoot = False
    #             else:
    #                 self.shoot = False
    #         else:
    #             self.shoot = False
    #         if self.shoot == True:
    #             if self.time < 600:
    #                 print ("Rev wheels")
    #                 self.Shooter.update(False, True, False, False)
    #             elif self.time < 750:
    #                 print ("shooting")
    #                 self.Shooter.update(False, True, True, False)
    #             else:
    #                 self.Shooter.update(False, False, False, False)
    #     self.FilterDrive.drive(0, 0, self.turn)
    
    
    def teleopInit(self):
        self.Drive.zeroEncoderTargets()
        self.readyToShoot = False
    
    def teleopPeriodic(self):
        averageFlySpeed = ( abs(self.LeftFly.getEncVelocity())
                          + abs(self.RightFly.getEncVelocity()) ) / 2
        # print(str(self.Vision.centerX()))
        print ("FlyWheelSpeed is : " + str(averageFlySpeed))

        if self.USING_GAMEPAD == False: # using joystick
            self.TurnJoy.updateButtons();
            self.MoveJoy.updateButtons();
            turn = -self.TurnJoy.getX()
            magnitude = self.MoveJoy.getMagnitude()
            direction = self.MoveJoy.getDirection()
            self.FilterDrive.drive(magnitude, direction, turn) # jeff mode
            self.Shooter.update(self.MoveJoy.getRawButton(2),\
                            self.MoveJoy.getRawButton(3),\
                            self.MoveJoy.getTrigger(),\
                            self.MoveJoy.getRawButton(5))
            
        else: # using gamepad
            if not self.Vision.centerX().__len__() == 0:
                self.needed = abs(self.Vision.centerX()[0] - 240)
                print (self.needed)
                if self.needed > 50:
                    self.turnSpeed = self.needed * .009
                else:
                    self.turnSpeed = self.needed * .0008
                if self.ShootGamepad.getRawButton(Gamepad.RB):
                    # TODO: move 240 to center pixel constant
                    if abs(self.Vision.centerX()[0] - 240) < 15:
                        self.readyToShoot = True
                    elif self.Vision.centerX()[0] - 240 > 0:
                        self.FilterDrive.drive(0, 0, -self.turnSpeed)
                        self.readyToShoot = False
                    elif self.Vision.centerX()[0] - 240 < 0:
                        self.FilterDrive.drive(0, 0, self.turnSpeed)
                        self.readyToShoot = False
                    else:
                        self.readyToShoot = False
            else:
                self.readyToShoot = False
            
            # TODO: what does this do??
            if self.readyToShoot and self.AUTO_SHOOT_ENABLED:
                if averageFlySpeed < 1900:
                    self.LeftFly.set(2000)
                    self.RightFly.set(-2000)
                elif averageFlySpeed > 1900:
                    self.LeftFly.set(2000)
                    self.RightFly.set(-2000)
                    self.Intake.set(1)
                else:
                    self.Shooter.update(False, False, False, False)
            
            if self.MoveGamepad.getRawButton(Gamepad.LJ): # faster button
                self.slowed = 1
            elif self.MoveGamepad.getRawButton(Gamepad.LB): # slower button
                self.slowed = .2
            else: # no button pressed
                # TODO: move to constant
                self.slowed = .55
            
            # switch drive mode with gamepad
            if   self.MoveGamepad.getRawButton(Gamepad.A):
                self.FilterDrive.setDriveMode(DriveInterface.DriveMode.VOLTAGE)
            elif self.MoveGamepad.getRawButton(Gamepad.B):
                self.FilterDrive.setDriveMode(DriveInterface.DriveMode.SPEED)
            elif self.MoveGamepad.getRawButton(Gamepad.X):
                self.FilterDrive.setDriveMode(DriveInterface.DriveMode.POSITION)
            
            turn = -self.MoveGamepad.getRX() \
                * abs(self.MoveGamepad.getRX()) * (self.slowed / 2)
            magnitude = self.MoveGamepad.getLMagnitude()**2 * self.slowed
            direction = self.MoveGamepad.getLDirection()
            
            if self.MoveGamepad.getRawButton(Gamepad.RB): # reverse direction
                direction += math.pi
            
            self.FilterDrive.drive(magnitude, direction, turn)
            
            self.Shooter.update(self.ShootGamepad.getRawButton(Gamepad.B),\
                                self.ShootGamepad.getRawButton(Gamepad.X),\
                                self.ShootGamepad.getRawButton(Gamepad.A),\
                                self.ShootGamepad.getRawButton(Gamepad.Y))

if __name__ == "__main__":
    wpilib.run(MainRobot)
