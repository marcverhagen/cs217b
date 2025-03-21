"""

Very simple example, just starting threads and have the main thread wait for them
to finish.

"""

import time
import threading

WAIT = True
#WAIT = False


def print_square(num):
    print(threading.current_thread().name)
    time.sleep(1)
    print("Square: {}" .format(num * num))


def print_cube(num):
    print(threading.current_thread().name)
    print("Cube: {}" .format(num * num * num))


if __name__ =="__main__":

    print('Defining threads')
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))
    print('Starting threads')
    t1.start()
    t2.start()
    if WAIT:
        t1.join()
        t2.join()
    print("Done")
