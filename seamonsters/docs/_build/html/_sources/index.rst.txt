Welcome to the seamonsters library documentation!
=================================================

This is Team 2605's Python library for robot code. It builds on wpilib and adds
useful utilities for working with input, motors, drivetrains, and Nav6's, as
well as for simulation without a robot and for quick and simple tests.

Terminology
-----------
In the documentation you will see the terms "position mode", "incremental 
position mode", and "jeff mode" used interchangeably. "Voltage mode" is used to
refer either to Voltage or PercentVbus mode on CANTalons. Also, some classes use
"velocity" in method/variable names while others use "speed."

Rebuilding the documentation
----------------------------
This documentation was created with Sphinx. To update it, navigate to
``seamonsters/docs`` and run ``make html``.

Modules:
--------

.. toctree::
   :maxdepth: 2

   commands
   dashboard
   drive
   gamepad
   holonomicDrive
   joystick
   logging
   modularRobot
   motorControl
   nav6
   path
   pdp
   swerveDrive
   utilityBots
   wpilib_sim


Indices
-------
- :ref:`genindex`
- :ref:`modindex`
- :ref:`search`

