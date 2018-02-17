:: Based on deploy.sh

setlocal
set file="robot.py"

if not "%1"=="" (
	set file=%~1
)

echo Deploying robot %file%

py "%file%" deploy --builtin --nonstandard && (
	pause
) || (
	python "%file%" deploy --builtin --nonstandard
	pause
)