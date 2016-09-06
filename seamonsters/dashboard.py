__author__ = "jacobvanthoog"

import wpilib

class DashboardBoolean:
    """
    References a single boolean value in the SmartDashboard
    """
    def __init__(self, key):
        self.key = key
        
    def get(self, *args, **kwargs):
        """
        Get the value. Specify ``defaultValue`` for a value to return if the key
        is not set. Otherwise a KeyError will be thrown.
        """
        return wpilib.SmartDashboard.getBoolean(self.key, *args, **kwargs)
        
    def set(self, value):
        """
        Set the value.
        """
        wpilib.SmartDashboard.putBoolean(self.key, value)

class DashboardDouble:
    """
    References a single Double value in the SmartDashboard
    """
    def __init__(self, key):
        self.key = key
        
    def get(self, *args, **kwargs):
        """
        Get the value. Specify ``defaultValue`` for a value to return if the key
        is not set. Otherwise a KeyError will be thrown.
        """
        return wpilib.SmartDashboard.getDouble(self.key, *args, **kwargs)
        
    def set(self, value):
        """
        Set the value.
        """
        wpilib.SmartDashboard.putDouble(self.key, value)

class DashboardInt:
    """
    References a single integer value in the SmartDashboard
    """
    def __init__(self, key):
        self.key = key
        
    def get(self, *args, **kwargs):
        """
        Get the value. Specify ``defaultValue`` for a value to return if the key
        is not set. Otherwise a KeyError will be thrown.
        """
        return wpilib.SmartDashboard.getInt(self.key, *args, **kwargs)
        
    def set(self, value):
        """
        Set the value.
        """
        wpilib.SmartDashboard.putInt(self.key, value)

class DashboardNumber:
    """
    References a single number value in the SmartDashboard
    """
    def __init__(self, key):
        self.key = key
        
    def get(self, *args, **kwargs):
        """
        Get the value. Specify ``defaultValue`` for a value to return if the key
        is not set. Otherwise a KeyError will be thrown.
        """
        return wpilib.SmartDashboard.getNumber(self.key, *args, **kwargs)
        
    def set(self, value):
        """
        Set the value.
        """
        wpilib.SmartDashboard.putNumber(self.key, value)

class DashboardString:
    """
    References a single string value in the SmartDashboard
    """
    def __init__(self, key):
        self.key = key
        
    def get(self, *args, **kwargs):
        """
        Get the value. Specify ``defaultValue`` for a value to return if the key
        is not set. Otherwise a KeyError will be thrown.
        """
        return wpilib.SmartDashboard.getString(self.key, *args, **kwargs)
        
    def set(self, value):
        """
        Set the value.
        """
        wpilib.SmartDashboard.putString(self.key, value)
