# CLASSES AS DECORATORS

# When a class name is given as a decorator, then you want the class to have a
# __call__ method. The function to be decorated is handed in as the argument to
# the __init__ method. The decorated function is actually not a function, but a
# class instance that acts as a function because of its __call__ method.

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
def slow_function(*args):
    time.sleep(1)
    print(f'Ran slow_function() over {args}')
    return True


print(f'\n{"="*80}\ndecorators8()\n{"="*80}\n')

print(slow_function)
print()
r1 = slow_function(1,2,3)
print(r1)
r2 = slow_function()
print(r2)

Timer.report()
print()