# Notes on Commands and Subsystems in pyfrc

## Subsystems

Subsystems represent integrated systems made up of components and serving a
single purpose, e.g. the drivetrain of the robot. A command can require a
subsystem to exclude other commands from using that subsystem's components. 

Subsystem code should include:
- initializing the controller classes associated with the individual components
  (Talons, sensors, etc.)
- performing utility actions: setting a whole side of the robot to drive forward
  at the same speed, etc.
- specifying a default command to run when no other commands are requiring the
  subsystem

## Commands

Commands represent robot actions. Commands may be atomic (drive the robot
forward for 2 seconds; move an arm to a setpoint) or continuous (listen for
joystick input and drive the robot in response).

Atomic commands must: 
- require a subsystem. This prevents separate commands that use the subsystem
  from conflicting.
- define an end state. This might be that the subsystem is within an acceptable
  range of its target, or that a certain amount of time has passed, etc.

## Open issues

- Need an easy way to run subsets of the robot, such as a prototype with only an
  arm and no drive system, etc.
