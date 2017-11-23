__author__ = "seamonsters"

COMMAND_LOGGING = True

class Command:

    STOPPED = 0
    STARTING = 1
    RUNNING = 2

    def __init__(self):
        self.state = Command.STOPPED
        self.time = 0
        self._interrupt = False

    # METHODS TO REPLACE

    def __repr__(self):
        return type(self).__name__

    def initialize(self):
        """
        Called when the command is started.
        """

    def execute(self):
        """
        Called continuously, 50 times per second as the command is running.
        """

    def isFinished(self):
        """
        Check if the command is finished.
        :return: True if the command is complete
        """
        return False

    def end(self):
        """
        Called when the command completes.
        """

    # UTILITY METHODS (DON'T REPLACE)

    def interrupt(self):
        """
        Cause the command to end early
        """
        self._interrupt = True

    # INTERNAL METHODS

    def _initialize(self):
        self.state = Command.RUNNING
        self.time = 0
        if COMMAND_LOGGING:
            print("Start: " + str(self))
        self.initialize()

    def _execute(self):
        self.execute()
        self.time += 1

    def _isFinished(self):
        if self._interrupt:
            self._interrupt = False
            return True
        return self.isFinished()

    def _end(self):
        self.state = Command.STOPPED
        if COMMAND_LOGGING:
            print("End: " + str(self))
        self.end()

    def start(self):
        """
        Used internally. Mark the command as started.
        """
        self.state = Command.STARTING

    def run(self):
        """
        Used internally. Perform a single step of the command.

        :returns: if the command is still running
        """
        if self.state == Command.STOPPED:
            return False
        if self.state == Command.STARTING:
            self._initialize()
        self._execute()
        if self._isFinished():
            self._end()
            return False
        return True


class CommandGroup(Command):

    class Entry:
        SEQUENTIAL = 0
        PARALLEL = 1

        def __init__(self, command, state):
            self.command = command
            self.state = state

    def __init__(self, name="Group"):
        super().__init__()
        self.name = name
        self.entries = []
        self.runningCommands = []
        self.currentCommandIndex = None

    def __repr__(self):
        return self.name

    def clear(self):
        self.entries.clear()

    def addSequential(self, command):
        if command is None:
            raise ValueError("Given None command")

        self.entries.append(
            CommandGroup.Entry(command, CommandGroup.Entry.SEQUENTIAL))

    def addParallel(self, command):
        if command is None:
            raise ValueError("Given None command")

        self.entries.append(
            CommandGroup.Entry(command, CommandGroup.Entry.PARALLEL))

    def _initialize(self):
        super()._initialize()
        self.currentCommandIndex = None

    def _execute(self):
        super()._execute()

        startNextCommand = False
        toRemove = [ ]
        for i, cmd in enumerate(self.runningCommands):
            if not cmd.run():
                toRemove.append(i)
                if i == len(self.runningCommands) - 1:
                    startNextCommand = True
                    self.currentCommandIndex += 1

        for i in reversed(toRemove):
            del self.runningCommands[i]

        if self.currentCommandIndex is None:
            self.currentCommandIndex = 0
            startNextCommand = True

        while startNextCommand and \
                        self.currentCommandIndex < len(self.entries):
            entry = self.entries[self.currentCommandIndex]
            entry.command.start()
            commandEnded = not entry.command.run()

            if commandEnded:
                self.currentCommandIndex += 1
            elif entry.state == CommandGroup.Entry.PARALLEL:
                self.runningCommands.append(entry.command)
                self.currentCommandIndex += 1
            else:
                self.runningCommands.append(entry.command)
                startNextCommand = False

    def _end(self):
        for cmd in self.runningCommands:
            cmd.interrupt()
            cmd.run()
        self.runningCommands.clear()

        super()._end()

    def isFinished(self):
        """Returns True if all the Commands in this group
        have been started and have finished.

        Teams may override this method, although they should probably
        reference super().isFinished() if they do.

        :returns: whether this CommandGroup is finished
        """
        return len(self.runningCommands) == 0


class WaitCommand(Command):

    def __init__(self, waitTime):
        super().__init__()
        self.waitTime = waitTime

    def __repr__(self):
        return "Wait " + str(self.waitTime)

    def isFinished(self):
        return self.time > self.waitTime


class PrintCommand(Command):

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __repr__(self):
        return "Print " + repr(self.message)

    def initialize(self):
        print(self.message)

    def isFinished(self):
        return True


class CommandWrapper(Command):
    """
    Wraps another command. This is meant to be extended to do useful things.
    """

    def __init__(self, command):
        super().__init__()
        self.command = command

    def __repr__(self):
        return type(self).__name__ + " (" + str(self.command) + ")"

    def initialize(self):
        self.command.time = 0
        self.command.initialize()

    def execute(self):
        self.command.state = self.state
        self.command.time = self.time
        self.command.execute()

    def isFinished(self):
        return self.command.isFinished()

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
        self.watchCommandStarted = False

    def initialize(self):
        self.watchCommandStarted = False

    def isFinished(self):
        if self.watchCommand.state != Command.STOPPED:
            self.watchCommandStarted = True
        return self.watchCommandStarted and self.watchCommand.isFinished()
