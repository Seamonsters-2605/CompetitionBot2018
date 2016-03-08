__author__ = "jacobvanthoog"
import wpilib
import math

ROTATION_TICKS_CAN1 = 131072 # encoder ticks in a full rotation
ROTATION_TICKS_CAN2 = 756
COMPLETED_DISTANCE = 0.06 # when both motors are within this fraction of their full ticks
                       # the movement has completed

class ArmReplay:

    # can1 is the motor at the base of the arm
    # can2 is the motor at the joint1
    def __init__(self, can1, can2):
        self.CAN1 = can1
        self.CAN2 = can2
        self.ensureControlMode(self.CAN1)
        self.CAN2.changeControlMode(wpilib.CANTalon.ControlMode.Speed)

        # target position of the encoders
        self.CAN1Target = self.CAN1.getEncPosition()
        self.CAN2Target = self.CAN2.getEncPosition()

        self.zero()

        self.CAN1Velocity = 2000 # ticks per step
        self.CAN2Velocity = 100

        self.MovementCompleted = False


    # should be called once per loop!
    def update(self):
        #print(self.rotateToPosition1(self.CAN1, self.CAN1Target), self.rotateToPosition2(self.CAN2, self.CAN2Target))
        self.rotateToPosition1(self.CAN1, self.CAN1Target)
        self.rotateToPosition2(self.CAN2, self.CAN2Target)
        self.MovementCompleted = \
            self.canMovementCompleted(self.CAN1, self.CAN1Target) and \
            self.canMovementCompleted(self.CAN2, self.CAN2Target)
        #if(self.MovementCompleted):
            #print("The movement has complete!")

    def setTarget(self, position):
        selfMovementCompleted = False
        self.CAN1Target = position[0] + self.CAN1Zero
        self.CAN2Target = position[1] + self.CAN2Zero
        print(position[0], position[1])
        #self.MovementComplete = False
        #print("Target set to:", position[0], position[1])

    def getTarget(self):
        return(self.CAN1Target - self.CAN1Zero, self.CAN2Target - self.CAN2Zero)

    def getPositions(self):
        return (self.CAN1.getEncPosition() - self.CAN1Zero, self.CAN2.getEncPosition() - self.CAN2Zero)

    def movementCompleted(self):
        return self.MovementCompleted

    def zero(self):
        self.CAN1Zero = self.CAN1.getEncPosition()
        self.CAN2Zero = self.CAN2.getEncPosition()


    # DON'T USE THESE

    def ticksPerRotation(self, can):
        if can == self.CAN1:
            return ROTATION_TICKS_CAN1
        if can == self.CAN2:
            return ROTATION_TICKS_CAN2
        return None

    def target(self, can):
        if can == self.CAN1:
            return self.CAN1Target
        if can == self.CAN2:
            return self.CAN2Target
        return None

    def velocity(self, can):
        if can == self.CAN1:
            return self.CAN1Velocity
        if can == self.CAN2:
            return self.CAN2Velocity
        return None

    def zeroPosition(self, can):
        if can == self.CAN1:
            return self.CAN1Zero
        if can == self.CAN2:
            return self.CAN2Zero
        return None

    def ensureControlMode(self, can):
        if not (can.getControlMode() == wpilib.CANTalon.ControlMode.Position):
            can.changeControlMode(wpilib.CANTalon.ControlMode.Position)
    
    def rotateToPosition1(self, can, target):
        current = can.getEncPosition()
        
        #if current == target:
            #print("At position")
            #can.set(current)
            #return(0)
        
        distance = (target - current) # amount motor should rotate

        value = 0
        if abs(distance) < self.velocity(can):
            value = target
        else:
            if distance > 0:
                value = current + self.velocity(can)
            else:
                value = current - self.velocity(can)

        #print(current, target, distance, value)
        
        can.set(-value)
        return(distance)

    def rotateToPosition2(self, can, target):
        current = can.getEncPosition()
        target = target
        if current == target:
            #print("At position")
            can.set(0)
            return(0)
        
        distance = target - current # amount motor should rotate
        
        if abs(distance) < self.velocity(can):
            pass
        else:
            if distance > 0:
                distance = self.velocity(can)
            else:
                distance = -self.velocity(can)

        #print(distance)
        
        can.set(-distance/2)
        return(distance)

    def canMovementCompleted(self, can, target):
        #print (abs(can.getEncPosition() - target) / self.ticksPerRotation(can))
        return abs(can.getEncPosition() - target) <= (COMPLETED_DISTANCE * self.ticksPerRotation(can))
