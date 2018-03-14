def visionTargetMode(table):
    table.putNumber('ledMode', 0) # on
    table.putNumber('pipeline', 1)

def driverCameraMode(table):
    table.putNumber('ledMode', 1) # off
    table.putNumber('pipeline', 0)

def cubeAlignMode(table):
    table.putNumber('ledMode', 0) # on
    table.putNumber('pipeline', 2)
