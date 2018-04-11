__author__ = "seamonsters"

from networktables import NetworkTables

logStates = { }

def sendLogStates():
    """
    Send all LogStates that have been updated to the dashboard
    :return:
    """
    global logStates
    logStateNames = [key for key, value in logStates.items()]
    logStateValues = [value for key, value in logStates.items()]
    table = NetworkTables.getTable('dashboard')
    table.putStringArray('logstatenames', logStateNames)
    table.putStringArray('logstatevalues', logStateValues)

class LogState:
    """
    Represents a value important to the user that is constantly changing.
    Whenever the value changes its new value will be printed to the console.
    There are checks to make sure that the same value isn't logged multiple
    times in a row (unless it changed and changed back), and to make sure that
    nothing is logged more than 2.5 times per second.
    """
    
    def __init__(self, name, logFrequency=0.4):
        """
        Initialize the LogState. ``name`` is the name of the value as printed
        in the console - it has no meaning other than that. ``logFrequency`` can
        be optionally given to specify the minimum number of seconds allowed
        between logs. The default value is 0.4 seconds, or 2.5 times per second.
        """
        self.name = name
        self.lastValue = ""
        self.valueChanged = False
        self.logFrequency = logFrequency
        # make sure the first value is logged
        self.timeSinceLastLog = self.logFrequency * 50 + 1
        
    def update(self, value):
        """
        Update the value to log. This should be called every loop (50 times per
        second) even if the value does not change. It's up to the LogState to
        determine if the value has changed.
        """
        global logStates
        
        value = str(value)
        logStates[self.name] = value
        if value != self.lastValue:
            self.lastValue = value
            self.valueChanged = True
        # 50 loops per second
        if self.valueChanged \
                and self.timeSinceLastLog >= self.logFrequency * 50:
            print(self.name + ": " + self.lastValue)
            self.timeSinceLastLog = 0
            self.valueChanged = False
        self.timeSinceLastLog += 1


# Logging test
# The correct output should be:
# Test 1
# test: 0
# test: 20
# test: 40
# test: 60
# test: 80
# Test 2
# test: 100
# Test 3
# test: 0
# test: 0
if __name__ == "__main__":
    log = LogState("test")
    print("Test 1")
    for i in range(0, 100):
        log.update(i)
    print("Test 2")
    for i in range(0, 100):
        log.update(100)
    print("Test 3")
    log.update(0)
    log.update(1)
    log.update(2)
    for i in range(0, 100):
        log.update(0)
    
