from contextlib import ExitStack
import time


class Timer:
    """A timer context to monitor time easily.

    Args:
        accumulate (bool) : Accumulate the time over multiple invocations (default: false)

    Example:
        timer = Timer()

        with timer:
            do_something
            do_something_else
        print(timer.time)              # print the time taken
        print(timer.as_dict)           # prints {"time": time_taken}

        timer = Timer(True)     # accumulate time
        with timer:
            do_something

        with timer:             # doesn't reset
            do_something_else

        print(timer.time)
        timer.clear()           # now reset
    """
    def __init__(self, accumulate: bool = False):
        self._accumulate = accumulate
        self._time = 0

    def __enter__(self):
        self._start = time.time()

    def __exit__(self, *args):
        if self.accumulate:
            self._time += time.time() - self._start
        else:
            self._time = time.time() - self._start

    def clear(self):
        self._time = 0

    @property
    def time(self):
        return self._time

    @property
    def accumulate(self):
        return self._accumulate

    @property
    def as_dict(self):
        return {"time": self._time}


def call_with_contexts(func, contexts, *args, **kwargs):
    with ExitStack() as stack:
        for con in contexts:
            stack.enter_context(con)
        func(*args, **kwargs)
