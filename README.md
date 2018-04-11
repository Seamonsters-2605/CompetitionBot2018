# Seamonsters Robot Code Template

Template for robot code.

Deploy with `./deploy.sh` or `.\deploy.bat` (Windows). Test with `./test.sh` or
`.\test.bat` (Windows).

## Directory Structure

- `seamonsters/`: The seamonsters library code. It has its own documentation, in
    `seamonsters/docs/_build/html/index.html` (you can view it online
    [here](https://rawgit.com/Seamonsters-2605/SeamonstersTemplate/master/seamonsters/docs/_build/html/index.html))
- `tests/`: Created and used by pyfrc for tests.
- `deploy.bat` and `deploy.sh`: Windows and Bash versions of scripts for
    deploying code to robot.
- `fastdeploy.bat` and `fastdeploy.sh`: Deploy code without testing it.
- `physics.py` and `sim/`: Used for pyfrc robot simulation. See `sim/README` for details.
