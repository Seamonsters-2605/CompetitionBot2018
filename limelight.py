def visionTargetMode(table):
    table.putNumber('pipeline', 1)
    table.putNumber('ledMode', 0) # on

def driverCameraMode(table):
    table.putNumber('pipeline', 0)
    table.putNumber('ledMode', 1) # off

def cubeAlignMode(table):
    table.putNumber('pipeline', 2)
    table.putNumber('ledMode', 1) # off
