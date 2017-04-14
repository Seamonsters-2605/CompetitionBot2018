__author__ = "jacobvanthoog"

# This is a quick and temporary solution for code that was written before
# CANTalons moved from wpilib to robotpy-ctre.

import wpilib
import ctre

wpilib.CANTalon = ctre.CANTalon
