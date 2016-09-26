python robot.py deploy --builtin --nc --skip-tests && (
	pause
) || (
	py robot.py deploy --builtin --nc --skip-tests
	pause
)