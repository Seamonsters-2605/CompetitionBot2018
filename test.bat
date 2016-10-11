:: Based on deploy.sh

setlocal
set file="robot.py"

if not "%1"=="" (
	set file=%~1
)

echo Testing robot %file%

py "%file%" test && (
	pause
) || (
	python "%file%" test
	pause
)