__author__ = "jacobvanthoog"

import wpilib

ROTATION_TICKS = 131072 # encoder ticks in a full rotation
COMPLETED_DISTANCE = 0.06
# when both motors are within this fraction of their full ticks
# the movement has completed

class ArmReplay:
    
    def __init__(self, can):
        self.CAN = can
        self.CAN.changeControlMode(wpilib.CANTalon.ControlMode.Position)

        # target position of the encoders
        self.Target = self.CAN.getEncPosition()
        self.zero()

        self.Velocity = 2000 # ticks per step
    
    # should be called once per loop!
    def update(self):
        self.rotateToPosition1(self.CAN, self.Target)
    
    def setTarget(self, position):
        self.Target = position + self.Zero
        print("Target set: ", position)
    
    def getTarget(self):
        return self.Target - self.Zero
    
    def moveTarget(self, amount):
        self.setTarget(self.getTarget() + amount)
    
    def getPosition(self):
        return self.CAN.getEncPosition() - self.Zero
    
    def movePosition(self, amount):
        self.setTarget(self.getPosition() + amount)
    
    def zero(self):
        self.Zero = self.CAN.getEncPosition()
    
    def movementCompleted(self, can, target):
        return abs(self.CAN.getEncPosition() - target)\
            <= (COMPLETED_DISTANCE * ROTATION_TICKS)
    
    # DON'T USE THESE
    
    def rotateToPosition1(self, can, target):
        current = can.getEncPosition()
        
        #if current == target:
            #print("At position")
            #can.set(current)
            #return(0)
        
        distance = (target - current) # amount motor should rotate
        
        value = 0
        if abs(distance) < self.Velocity:
            value = target
        else:
            if distance > 0:
                value = current + self.Velocity
            else:
                value = current - self.Velocity
                
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
        
        if abs(distance) < (self.Velocity):
            pass
        else:
            if distance > 0:
                distance = self.Velocity
            else:
                distance = -self.Velocity
                
        #print(distance)
        
        can.set(-distance/2)
        return(distance)

