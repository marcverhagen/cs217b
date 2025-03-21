"""

Using the multiprocessing module which has a Pool class for processes and a
ThreadPool class for threads.

"""

from multiprocessing.pool import ThreadPool

def square(num):
    return num * num

pool = ThreadPool(processes=1)

result = pool.apply_async(square, (4,))

print(result, '-->', result.get())
