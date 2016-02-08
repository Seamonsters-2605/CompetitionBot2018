HolonomicDrive.py
~Dawson Bowhay

/////////////////////////////////////////////////////////////////////////////////////////////

Important note: A positive direction around the unit circle is positive turn. Keep this in
mind. If you do this right and control it with regular magnitude and direction, everything
will either be forwards or everything will be backwards, depending on which direction is
default for your motors/motor controllers. If everything is backwards, use the invertDrive()
function.

/////////////////////////////////////////////////////////////////////////////////////////////

Details:
-Code for Mecanum/Omni drives in the "diamond" configuration ("x" config is like never used)
-Has class variable for offset of wheels. Default is .25 pi radians (or 45 degrees), which is
ideal for our regular mecanum wheels or the typical omni drive's (but not Jeff's)
-If you want this code to work with Jeff's drivetrain just change the angle offset to 27/180
pi radians (27 degrees) using the builtin function. The transition between the 2 drivetrains
should take 1 line of code

/////////////////////////////////////////////////////////////////////////////////////////////

Version:
-This is version 1.1 and a few bugs have been fixed including a function name that matched a
class variable name
-There is still more stuff to be implemented
-The default max velocity is 2000 right now, which isn't super fast

/////////////////////////////////////////////////////////////////////////////////////////////

Functions(that you should actually use, not all functions):

-driveVoltage(magnitude, direction, turn)
This function is used for driving in percentVBus mode

-driveSpeed(magnitude, direction, turn)
This function is used for driving in speed mode (w/encoders hooked up)

-invertDrive()
This function inverts everything. It will probably be used.

-setWheelOffset(angleInRadians)
This function should be used to set the offset angle at which your wheels exert force.
To do a tank drive just set it to zero (LOL why wouldn't you just use code designed for a
tank drive?). Typical omni/mecanum setups are .25 pi radians (which is the defualt)

-setMaxVelocity(velocity)
Sets the max encoder velocity to a different number. Default is 1000.
