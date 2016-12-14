:: Based on fastdeploy.sh

setlocal
set file="robot.py"

if not "%1"=="" (
	set file=%~1
)

echo Deploying robot %file%

py "%file%" deploy --builtin --nc --skip-tests --no-version-check && (
	pause
) || (
	python "%file%" deploy --builtin --nc --skip-tests --no-version-check
	pause
)
