seamonsters.utilityBots
=======================

This module contains very basic robot implementations for testing things. These
must be subclassed with a bit of extra code to be used. Make sure if you define
``__init__``, or special robot functions like ``robotInit``, etc., that you also
call ``super()``'s versions of those functions.

driveTest
---------
Lets you test a DriveInterface (see ``seamonsters.drive.DriveInterface``).

In robotInit, call ``super().robotInit()``, then
``super().initDrive(interface)``, where ``interface`` is a DriveInterface that
you have created.

You will then be able to drive around the robot using the left and right
joysticks on the gamepad. Press A, B, or X to switch between Voltage, Speed, and
Position mode. Hold the left joystick to go faster, and the left bumper to go
slower.

encoderTest
-----------
In ``__init__``, call ``super().__init__(ports)``, where ``ports`` is an array
of port numbers. While in teleop mode the encoder positions will be printed
continuously.

pidTest
-------
For experimenting with PID's.

In robotInit, call
``super().robotInit(talonPort, [ticksPerRotation, maxVelocity])``, where
``talonPort`` is the port of the motor to test. ``ticksPerRotation`` and
``maxVelocity`` are optional.

Instructions will be printed to the console for how to use it. You will need a
single joystick.