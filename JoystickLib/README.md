# JoystickLib

This library has a single class, `JoystickUtils`, which wraps pyfrc's `Joystick` class. The main additions are a "dead-zone" for the position of the joystick, and events that occur when a button is pressed or released.

Method names in JoystickUtils mostly correspond with those in Joystick. Look [here](http://robotpy.readthedocs.org/en/latest/wpilib/Joystick.html) for documentation for the original Joystick class.

### Methods added:
- `updateButtons()` Should be called every `teleopPeriodic` loop - updates the current state of the buttons for events
- `buttonPressed(button)` Checks if the button was pressed since the last `updateButtons` call.
- `buttonReleased(button)` Checks if the button was released since the last `updateButtons` call.
