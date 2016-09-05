# Seamonsters Robot Code Template

Code for the JellyFISH!

Deploy with `./deploy.sh` or `.\deploy.bat` (Windows). Test with `./test.sh` or
`.\test.bat` (Windows).

## Terminology
In the documentation you will see the terms "position mode", "incremental 
position mode", and "jeff mode" used interchangeably. "Voltage mode" is used to
refer either to Voltage or PercentVbus mode on CANTalons. Also, some classes use
"velocity" in method/variable names while others use "speed."


## Directory Structure

- `seamonsters/`: The work-in-progress seamonsters library code.
    - `seamonsters/utilityBots/`: Very basic robot implementations for testing 
        things. These must be subclassed with a bit of extra code to be used.
    - `seamonsters/wpilib_sim/`: Robot simulation (work in progress), with
        rudimentary support for connecting to Blender physics simulation. If you
        import seamonsters.wpilib_sim.simulate, your robot will magically
        support simulation. To start in simulation mode, type
        `python3 robot.py wpilib_sim`, followed by:
        - Nothing: run robotInit and stop
        - `d`: Disabled mode
        - `a`: Autonomous mode
        - `t`: Teleop mode
        - `s`: Test mode
- `GRIP/`: GRIP files used in competition for image recognition.
- `Shooter/`: Code for the flywheels, intake motor, and "ShootController", which
    allows control of both.
- `tests/`: Created and used by pyfrc for tests.
- `Vision.py`: Simple code that gets the center of the target from GRIP (when it
    works).
- `robot.py`: The final robot, used in the 2016 competition and updated slightly
    since then.
- `testBot.py`: Robot that is modified for testing various things.
- `holoBot.py`: Simple bot used for testing holonomic drives.
- `swerveBot.py`: Simple bot used for testing swerve drives.
- `bTest.py`: Very simple bot that spins a single motor - used for testing
    Blender simulation.
- `deploy.bat` and `deploy.sh`: Windows and *nix versions of scripts for
    deploying code to robot.
- `test.bat` and `test.sh`: Scripts for testing robot code without needing an
    actual robot to deploy to.

## Subsystems

Subsystems represent integrated systems made up of components and serving a single purpose, e.g. the drivetrain of the robot. A command can require a subsystem to exclude other commands from using that subsystem's components. 

Subsystem code should include:
- initializing the controller classes associated with the individual components (Talons, sensors, etc.)
- performing utility actions: setting a whole side of the robot to drive forward at the same speed, etc.
- specifying a default command to run when no other commands are requiring the subsystem

## Commands

Commands represent robot actions. Commands may be atomic (drive the robot forward for 2 seconds; move an arm to a setpoint) or continuous (listen for joystick input and drive the robot in response).

Atomic commands must: 
- require a subsystem. This prevents separate commands that use the subsystem from conflicting.
- define an end state. This might be that the subsystem is within an acceptable range of its target, or that a certain amount of time has passed, etc.

## Open issues

- Need an easy way to run subsets of the robot, such as a prototype with only an arm and no drive system, etc.
