# Seamonsters Robot Code Template

Code for the JellyFISH!

Deploy with `./deploy.sh` or `.\deploy.bat` (Windows). Test with `./test.sh` or
`.\test.bat` (Windows).

## Directory Structure

- `seamonsters/`: The seamonsters library code. It has its own documentation, in
    `seamonsters/docs/_build/html/index.html`.
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
