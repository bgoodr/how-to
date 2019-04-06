import time


class TimeOnce:
    """Time a sequence of code, allowing access to the time difference in seconds.

    Example without exception:

        elapsed = TimeOnce()
        with elapsed:
            print('sleeping ...')
            time.sleep(3)
        print("elapsed", elapsed)

    Example with exception:

        elapsed = TimeOnce()
        try:
            with elapsed:
                print('sleeping ...')
                time.sleep(3)
                raise ValueError('foo')
            print("elapsed inner", elapsed)
        finally:
            print("elapsed outer", elapsed)
    """
    def __init__(self):
        self.t0 = None  # An invalid value.

    def __enter__(self):
        self.t0 = time.time()

    def __exit__(self, type, value, traceback):
        self.dt = time.time() - self.t0

    def get_elapsed(self):
        return self.dt

    def __str__(self):
        return str(self.dt)
