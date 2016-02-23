import networktables
from networktables import NetworkTable
class Vision():
    def __init__(self):
        self.table = NetworkTable.getTable("/GRIP/myContoursReport/")

    def centerX(self):
        numarray = networktables.NumberArray()
        if(self.table.containsKey("centerX")): # during testing, this stuff doesn't exist and it'll fail the tests
                                               # if we don't check first.
            self.table.retrieveValue("centerX", numarray)
            return numarray
        return []