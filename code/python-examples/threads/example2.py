"""

Adding an extra argument to the target function's definition in order to collect
the results. Needed because the start() method does not return anything.

"""

import threading


def print_cube(num, results):
    result = num * num * num
    results[threading.current_thread().name] = result
    print("Cube: {}" .format(result))


def print_square(num, results):
    result = num * num
    results[threading.current_thread().name] = result
    print("Square: {}" .format(result))


if __name__ =="__main__":

    results = {}
    t1 = threading.Thread(target=print_square, args=(10, results))
    t2 = threading.Thread(target=print_cube, args=(10, results))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(results)