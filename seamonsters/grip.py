__author__ = "jacobvanthoog"

import networktables
from networktables import NetworkTable

class GripInterface():
    """
    Simple methods for getting data from GRIP NetworkTables.
    """
    def __init__(self, networkTableName):
        self.table = NetworkTable.getTable("/GRIP/" + networkTableName + "/")

    def getKey(self, name):
        if(self.table.containsKey(name)):
            numArray = networktables.NumberArray()
            self.table.retrieveValue(name, numArray)
            return numArray
        else:
            return [ ]