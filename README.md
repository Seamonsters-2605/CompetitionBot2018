# Seamonsters Robot Code Template

Template for robot code.

Deploy with `./deploy.sh` or `.\deploy.bat` (Windows). Test with `./test.sh` or
`.\test.bat` (Windows).

## Directory Structure

- `seamonsters/`: The seamonsters library code. It has its own documentation, in
    `seamonsters/docs/_build/html/index.html` (you can view it online
    [here](https://rawgit.com/Seamonsters-2605/SeamonstersTemplate/master/seamonsters/docs/_build/html/index.html))
- `testBot.py`: Robot that is modified for testing various things.
- `holoBot.py`: Simple bot used for testing holonomic drives.
- `bTest.py`: Very simple bot that spins a single motor - used for testing
    Blender simulation.
- `deploy.bat` and `deploy.sh`: Windows and *nix versions of scripts for
    deploying code to robot.
- `fastdeploy.bat` and `fastdeploy.sh`: Deploy code without testing it.
- `test.bat` and `test.sh`: Scripts for testing robot code without needing an
    actual robot to deploy to.
