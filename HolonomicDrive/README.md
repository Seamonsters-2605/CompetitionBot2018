HolonomicDrive.py
~Dawson Bowhay

Details:
-Code for Mecanum/Omni drives in the "diamond" configuration ("x" config is like never used)
-Has class variable for offset of wheels. Default is .25 pi radians (or 45 degrees), which is
ideal for our regular mecanum wheels or the typical omni drive's (but not Jeff's)
-If you want this code to work with Jeff's drivetrain just change the angle offset to 27/180
pi radians (27 degrees) using the builtin function. The transition between the 2 drivetrains
should take 1 line of code

/////////////////////////////////////////////////////////////////////////////////////////////
Version:
-This is the first version and I just tested it yesterday so there could be some undiscovered
bugs
-There is still more stuff to be implemented like toggling break mode, some kind of kill
function, etc.
-The default max velocity is 1000 right now, which is pretty slow. This needs to be tested
and improved

/////////////////////////////////////////////////////////////////////////////////////////////
Functions(that you should actually use, not all):

-driveVoltage(magnitude, direction, turn)
This function is used for driving in percentVBus mode

-driveSpeed(magnitude, direction, turn)
This function is used for driving in speed mode (w/encoders hooked up)

-invert()
This function inverts everything. Hopefully not needed...

-setWheelOffset(angleInRadians)
This function should be used to set the offset angle at which your wheels exert force.
To do a tank drive just set it to zero (LOL why wouldn't you just use code designed for a
tank drive?). Typical omni/mecanum setups are .25 pi radians (which is the defualt)

-setMaxVelocity(velocity)
Sets the max encoder velocity to a different number. Default is 1000.