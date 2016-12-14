# --builtin = Use built in tests
# --nc = Show robot stdout
# --nonstandard = Allow files other than robot.py
# --skip-tests
# --no-version-check = Don't check wpilib version

file=robot.py

if [ $# == 1 ]
    then
        file=$1
fi

echo Deploying robot $file

hash python3 2> /dev/null || {
    hash python 2> /dev/null || {
        hash py 2> /dev/null || {
            echo "Python not found!"
            exit 1
        }
        py $file deploy --builtin --nc --nonstandard --skip-tests --no-version-check
        exit 0
    }
    python $file deploy --builtin --nc --nonstandard --skip-tests --no-version-check
    exit 0
}
python3 $file deploy --builtin --nc --nonstandard --skip-tests --no-version-check
echo "Done, press enter to quit"
read
