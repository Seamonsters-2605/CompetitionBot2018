__author__ = 'Ian'
import math

import serial

from .nav6protocol import *
import threading
import wpilib.timer

#Notes Pitch and Roll need ranges mess with it appears they go from 0 to 90 to 0 on one part which doesn't make much
#sense.... Also the changing to 360 and offset functions could use some work as well.

class Nav6( ):
    def __init__( self, serialNumber, updateRate ):
        self.stopRequested = False
        #This is here in case we are testing one a pc so the code doesn't crash bc the Nav6 isn't connected.
        try:
            self.ser = serial.Serial(serialNumber,self.getDefaultBaudRate())
        except:
            self.ser = None

        self.updateRate = updateRate
        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.yOff = 0.0
        self.pOff = 0.0
        self.rOff = 0.0
        self.cHOff = 0.0
        self.compassHeading = 0.0
        self.isStopped = True

    def start( self ):
        self.stopRequested = False
        self.thread = threading.Thread(target=self.serialUpdate,name="Nav6")
        self.thread.start()
        wpilib.timer.Timer.delay(.3)
        self.zero()

    def stop( self ):
        self.stopRequested = True

    def zero(self):
        print('Zeroing Nav6')
        self.yOff = self.calcOffset(self.yaw)
        self.rOff = self.calcOffset(self.roll)
        self.pOff = self.calcOffset(self.pitch)
        self.cHOff = self.compassHeading

    def getRawYaw(self):
        return self.yaw

    def getRawPitch(self):
        return self.pitch

    def getRawRoll(self):
        return self.roll

    def getRawCompassHeading(self):
        return self.compassHeading

    def getYaw( self ):
        return self.applyOffset(self.yaw,self.yOff)

    def getPitch( self ):
        return self.applyOffset(self.pitch,self.pOff)

    def getRoll( self ):
        return self.applyOffset(self.roll,self.rOff)

    def getSerial( self ):
        return self.ser

    def getDefaultBaudRate( self ):
        return 57600

    def getCompassHeading( self ):
        return self.compassHeading - self.cHOff

    def sendStreamCommand( self, updateRate=10, streamType='y' ):
        buff = [ 0 ] * 9

        buff[ 0 ] = (PACKET_START_CHAR)
        buff[ 1 ] = (MSGID_STREAM_CMD)
        buff[ 2 ] = streamType

        self.setStreamUint8( buff, 3, updateRate )
        self.setStreamTermination( buff, 5 )

        strBuff = ''
        for item in buff:
            strBuff += item
        print( strBuff )

        barray = str.encode(strBuff)

        self.ser.write(barray)
        self.ser.flush()

    def serialUpdate( self ):
        self.isStopped = False
        responce = ""

        self.sendStreamCommand( self.updateRate )

        while (not self.stopRequested):
            self.ser.flushInput()
            responce = self.ser.readline()

            responce = responce.decode()

            if responce[0] != '!':
                continue

            if len(responce) == 34:
                self.decodeRegularResponse(responce)
            else:
                pass

            wpilib.timer.Timer.delay(.02)

        self.isStopped = True

    def decodeRegularResponse( self, strResponce ):
        self.yaw = float(strResponce[2:9])
        self.pitch = float(strResponce[9:16])
        self.roll = float(strResponce[16:23])
        self.compassHeading = float(strResponce[23:30])
        #print("Yaw: %f Pitch: %f Roll: %f"%(self.getYaw(),self.getPitch(),self.getRoll()))
        #print("Yaw: %f Pitch: %f Roll: %f"%(self.yOff,self.pOff,self.rOff))
        #print("Yaw: %f Pitch: %f Roll: %f"%(self.getRawYaw(),self.getRawPitch(),self.getRawRoll()))
        #print()

    def decodeQuaternionResponse( self, buffer, length ):
        pass

    def setStreamTermination( self, buffer, messageLength ):
        print( buffer )
        self.setStreamUint8( buffer, messageLength, self.calcaulteChecksum( buffer, messageLength ) )
        buffer[ messageLength + 2 ] = '\r'
        buffer[ messageLength + 3 ] = '\n'

    def calcaulteChecksum( self, buffer, length ):
        sum = 0
        for i in range( length ):
            sum += ord( buffer[ i ] )

        if sum >= 256:
            mult = sum // 256
            sum -= mult * 256

        return sum

    def calcOffset(self,ypr):
        if ypr == 0:
            return 0
        elif ypr < 0:
            return  360 - abs(ypr)
        return ypr

    def convertTo360(self,value):
        if value < 0:
            return 360 - abs(value)
        elif value > 0:
            return value
        elif value == 0:
            return 0

    def applyOffset(self, value, offset):
            value = self.convertTo360(value)
            value = value - offset
            if value < 0:
                return 360 - abs(value)
            return value

    def setStreamUint8( self, buffer, index, value ):
        hexref = '0123456789ABCDEF'
        buffer[ index + 1 ] = (hexref[ value & 0x0F ])
        buffer[ index ] = (hexref[ value >> 4 ])
