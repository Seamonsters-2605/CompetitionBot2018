# Seamonsters Robot Code Template

Template for robot code.

Deploy with `./deploy.sh` or `.\deploy.bat` (Windows). Test with `./test.sh` or
`.\test.bat` (Windows).

## Directory Structure

- `seamonsters/`: The seamonsters library
- `tests/`: Created and used by pyfrc for tests.
- `deploy.bat` and `deploy.sh`: Windows and Bash versions of scripts for
    deploying code to robot.
- `fastdeploy.bat` and `fastdeploy.sh`: Deploy code without testing it.
- `physics.py` and `sim/`: Used for pyfrc robot simulation. See `sim/README` for details.

## How to update the seamonsters library documentation

The built sphinx documentation is published using GitHub pages on the `gh-pages` branch. In `seamonsters/docs`, run `make clean`, then `make html` on that branch and push to update.

You can view the documentation [here](https://seamonsters-2605.github.io/SeamonstersTemplate/seamonsters/docs/_build/html/index.html).