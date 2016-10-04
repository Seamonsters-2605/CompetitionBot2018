seamonsters.wpilib_sim
======================

Robot simulation (work in progress), with rudimentary support for connecting to
Blender physics simulation. To use it, import
``seamonsters.wpilib_sim.simulate`` **before anything else**, and your robot
will magically support simulation. To start in simulation mode, type
``python3 robot.py wpilib_sim``, followed by:

- Nothing: run robotInit and stop
- ``d``: Disabled mode
- ``a``: Autonomous mode
- ``t``: Teleop mode
- ``s``: Test mode