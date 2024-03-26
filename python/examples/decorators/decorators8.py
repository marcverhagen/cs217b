# CLASSES AS DECORATORS

import time


class Timer:

    calls = 0
    total_time = 0

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        start_time = time.perf_counter()
        result = self.func(*args, **kwargs)
        elapsed_time = time.perf_counter() - start_time
        Timer.calls += 1
        Timer.total_time += elapsed_time
        print(f"Elapsed time: {elapsed_time:.6f} seconds")
        return result

    @classmethod
    def report(self):
        print(f"\nNumber of calls: {Timer.calls}")
        print(f"Total elapsed time: {Timer.total_time:.6f} ")


@Timer
def slow_function():
    import time
    time.sleep(1)

slow_function()
slow_function()
Timer.report()



