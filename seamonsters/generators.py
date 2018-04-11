__author__ = "seamonsters"

import types
import itertools

def sequence(*iterables):
    """
    Run a set of iterables sequentially
    """
    return itertools.chain(*iterables)

def parallel(*iterables):
    """
    Run a group of iterables in parallel. Ends when none are left running.

    If any iterable yields a function, it will be added to the set of running
    iterables.
    """
    return watch(*iterables, None)

def watch(*iterables):
    """
    Run a group of iterables in parallel. Ends when the last iterables in the
    given list has finished or yields True, regardless of the others.

    If any iterable yields a function, it will be added to the set of running
    iterables.
    """
    iterables = list(iterables)
    watch = iterables[-1]
    if watch == None:
        iterables = iterables[:-1]
    try:
        while len(iterables) != 0:
            toRemove = [ ]
            for iter in iterables:
                result = None
                try:
                    result = next(iter)
                except StopIteration as e:
                    if iter == watch:
                        return e.value
                    toRemove.append(iter)
                if result == True and iter == watch:
                    return
                if isinstance(result, types.GeneratorType):
                    iterables.append(result)
            for iter in toRemove:
                iterables.remove(iter)
            yield
    finally:
        for iter in iterables:
            iter.close()

def wait(time):
    """
    Wait for a certain number of iterations.
    """
    for _ in range(time):
        yield

def forever():
    """
    Iterate forever.
    """
    while True:
        yield

def timeLimit(iterable, time):
    """
    Run the iterable until it finishes or the given time limit has passed.
    Return the value of the iterable if it ends early, None otherwise.
    """
    return itertools.islice(iterable, time)

def untilTrue(iterable):
    """
    Run the iterable until it yields True, then stop.
    """
    return itertools.takewhile(lambda x: not x, iterable)

def ensureTrue(iterable, requiredCount):
    """
    Wait until the iterable yields True for a certain number of consecutive
    iterations before finishing.
    """
    count = 0
    for x in iterable:
        if x:
            count += 1
        else:
            count = 0
        if count > requiredCount:
            break
        yield

def returnValue(iterable, value):
    """
    Run an iterable but change the return value.
    :return: value
    """
    yield from iterable
    return value
