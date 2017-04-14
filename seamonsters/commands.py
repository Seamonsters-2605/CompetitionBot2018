__author__ = "seamonsters"

import wpilib.command

class CommandWrapper(wpilib.command.Command):
    """
    Wraps another command. This is meant to be extended to do useful things.
    """

    def __init__(self, command):
        super().__init__()
        self.command = command
        for requirement in self.command.getRequirements():
            self.requires(requirement)

    def initialize(self):
        self.command.initialize()

    def execute(self):
        self.command.execute()

    def isFinished(self):
        return self.command.isFinished()

    def interrupted(self):
        self.command.interrupted()

    def end(self):
        self.command.end()

class ForeverCommand(CommandWrapper):
    """
    Wraps a command. isFinished() always returns False.
    """

    def __init__(self, command):
        super().__init__(command)

    def isFinished(self):
        return False

class EnsureFinishedCommand(CommandWrapper):
    """
    Waits until isFinished() of the wrapped command returns True for a certain
    number of steps before finishing.
    """

    def __init__(self, command, requiredCount):
        super().__init__(command)
        self.requiredCount = requiredCount
        self.count = 0

    def isFinished(self):
        if self.command.isFinished():
            self.count += 1
        else:
            self.count = 0
        return self.count > self.requiredCount

class WhileRunningCommand(CommandWrapper):
    """
    Wraps one command, but tracks a different command (``watchCommand``) for
    isFinished().
    """

    def __init__(self, command, watchCommand):
        super().__init__(command)
        self.watchCommand = watchCommand

    def isFinished(self):
        return self.watchCommand.isFinished()
