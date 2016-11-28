# RobotSimulation
This library makes it easier to set up the robot simulator that's included in pyfrc.

## Installation instructions
 - Use pip3 to install `pyfrc`
 - Install tkinter for Python 3. On Linux you will need to install the tkinter package for Python 3 - it will be called something like `python3-tkinter`.
 - Use pip3 to install `pygame` if you want to use real joystick input
 - Add the "physics.py" file and the "sim" folder to the same directory as your robot.py

Run the simulation by typing `py -3 robot.py sim` in Windows, or `python3 robot.py sim` in Mac/Linux.

## Robots
An example robot.py file has been included.

All Talons should be in PercentVBus mode (the default). You can have other talons besides the drive train motors, but only those motors will be simulated.

At the bottom of the robot file you should have:

```
if __name__ == '__main__':
    wpilib.run(YourRobotClass, physics_enabled=True)
```

## Configuration files
The "sim" folder contains configuration files for the simulation. "drivetrain.ini" controls the physics of the drivetrain. "config.json" controls the visual layout of the field. Look at both for examples, or see details for each below.

### config.json
config.json is a JSON file. The structure is below:
- `pyfrc`: Object
    - `robot`: Object
        - `w`: Number; The distance between the front and back wheels, in feet.
        - `h`: Number; The distance between the right and left wheels, in feet.
        - `starting_x`: The starting x position of the robot, in feet to the right of the left edge of the field.
        - `starting_y`: The starting y position of the robot, in feet below the top edge of the field.
        - `starting_angle`: The starting angle of the robot, in degrees. 0 is facing right, positive numbers are clockwise.
    - `field`: Object
        - `w`: Number; The width of the field in feet.
        - `h`: Number; The height of the field in feet.
        - `px_per_ft`: Number; The scale of the field on the screen - how many screen pixels represent one foot.
        - `objects`: Array of objects that are drawn in the background on the field. For each object:
            - `color`: The color of the object. Some names are allowed, like `green` or `DarkOliveGreen`. A full list is [here](https://www.tcl.tk/man/tcl8.4/TkCmd/colors.htm).
            - `points`: An array. Each item is an array of 2 numbers, the x and y position of the point. Use at least 3 points to define a polygon, which will be drawn on the field.

### drivetrain.ini

drivetrain.ini is parsed using `configparser`, which allows [typical INI file structure](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure). A `[physics]` header is required at the top of the file. After that, values are stored as a list `name=value` lines. These can be in any order. Lines that start with a `#` will be ignored. The following values are used:

- `xlen=` Distance between right and left wheels (width), in feet. Default is 2.
- `ylen=` Distance between front and back wheels (length). Default is 3. The config.json file also has `w` and `h` values (width and height), however these only affect the visual appearance of the robot, and they are reversed from the equivalent drivetrain.ini values - set `w` to the `ylen` value, and `h` to the `xlen` value.
- `speed=` Speed of the robot in feet per second. 5 - 7 ft/s is a typical speed. Default is 6.
- `drivetrain=` The drivetrain type. Can be:
  - `drivetrain=mecanum` Mecanum drivetrain
  - `drivetrain=four` Four-motor drivetrain - the default
  - `drivetrain=two` Two-motor drivetrain

##### For four-motor and mecanum drivetrains:
- `canfl=` Port number of the front left motor
- `canfr=` Port number of the front right motor
- `canbl=` Port number of the back left motor
- `canbr=` Port number of the back right motor

##### For two-motor drivetrains:
- `canfl=` Port number of the left motor
- `canfr=` Port number of the right motor

Setting the port number values to negative numbers reverses the direction of the motor. The drivetrains in the simulation may have their motors oriented differently than a real robot, so you will have to experiment with reversing motors in the configuration file.

