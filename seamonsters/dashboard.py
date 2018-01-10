import networktables

def getSwitch(name, defaultValue):
    """
    Get whether a switch on the dashboard is enabled.
    """
    table = networktables.NetworkTables.getTable('dashboard')
    try:
        switchNames = table.getStringArray('switchnames')
        switchValues = table.getBooleanArray('switchvalues')
    except BaseException as e:
        print("Exception while getting switch", e)
        return defaultValue
    if not name in switchNames:
        print("Couldn't find switch name", name)
        return defaultValue
    if len(switchNames) != len(switchValues):
        print("Invalid switch data!")
        return defaultValue
    return switchValues[switchNames.index(name)]
