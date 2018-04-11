import networktables
import traceback

def getSwitch(name, defaultValue):
    """
    Get whether a switch on the dashboard is enabled.
    """
    table = networktables.NetworkTables.getTable('dashboard')
    try:
        switchNames = table.getStringArray('switchnames', [])
        switchValues = table.getBooleanArray('switchvalues', [])
    except BaseException as e:
        print("Exception while getting switch", e)
        return defaultValue
    if not name in switchNames:
        #print("Couldn't find switch name", name)
        return defaultValue
    if len(switchNames) != len(switchValues):
        print("Invalid switch data!")
        return defaultValue
    return switchValues[switchNames.index(name)]

def setActiveCameraURL(url):
    """
    Set the URL of the camera stream to display in the dashboard
    :param url: URL string
    """
    table = networktables.NetworkTables.getTable('dashboard')
    table.putString('cam', url)

class DashboardCommandReader:
    """
    Allows reading data entered in the Command box on the dashboard.
    """

    def __init__(self):
        self.commandTable = networktables.NetworkTables.getTable('commands')
        self.reset()

    def reset(self):
        """
        Reset the connection, forget existing commands.
        """
        self.lastCommandId = 0
        self.commandTable.putString('command', "")
        self.commandTable.putNumber('id', 0)

    def getCommand(self):
        """
        Get the command entered in the box.
        :return: a command string, or None if no command
        """
        try:
            commandId = self.commandTable.getNumber('id', 0)
            if commandId != self.lastCommandId:
                command = self.commandTable.getString('command', '')
                command = command.strip()
                self.lastCommandId = commandId
                if command != "":
                    return command
        except:
            traceback.print_exc()
        return None
