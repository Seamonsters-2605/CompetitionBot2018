# JoystickLib

This library has a single class, `JoystickUtils`, which wraps pyfrc's `Joystick` class. The main additions are a "dead-zone" for the position of the joystick, events that occur when a button is pressed or released, and the ability to invert the x or y axis of the joystick.

Method names in JoystickUtils mostly correspond with those in Joystick. Look [here](http://robotpy.readthedocs.org/en/latest/wpilib/Joystick.html) for documentation for the original Joystick class.

### Methods added:
- `updateButtons()` Should be called every `teleopPeriodic` loop - updates the current state of the buttons for events.
- `buttonPressed(button)` Checks if the button was pressed since the last `updateButtons` call.
- `buttonReleased(button)` Checks if the button was released since the last `updateButtons` call.
- `invertX(enabled=True)` Sets whether to invert the x axis. `enabled` is optional and defaults to True
- `invertY(enabled=True)` Sets whether to invert the y axis.
