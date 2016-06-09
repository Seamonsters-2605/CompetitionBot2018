file=robot.py

if [ $# == 1 ]
    then
        file=$1
fi

echo Testing robot $file

hash python3 2> /dev/null || {
    hash python 2> /dev/null || {
        hash py 2> /dev/null || {
            echo "Python not found!"
            exit 1
        }
        py $file test
        exit 0
    }
    python $file test
    exit 0
}
python3 $file test
