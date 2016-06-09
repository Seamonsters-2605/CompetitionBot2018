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
        py $file deploy --builtin --nc --nonstandard
        exit 0
    }
    python $file deploy --builtin --nc --nonstandard
    exit 0
}
python3 $file deploy --builtin --nc --nonstandard
echo "Done, press enter to quit"
read