"""

Subclassing Thread to store and return the return value of the target function.

https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread
(the above also overrides the __init__ method to define the new instance variable)

According to https://docs.python.org/3/library/threading.html you should only override
__init__() and run() so the post goes a little bit against that, but note that we could
get the return value from the thread so overriding join() was not necessary.

"""

from threading import Thread


def cube(num):
    return num * num * num

def square(num):
    return num * num


class ThreadWithReturnValue(Thread):
    
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


if __name__ =="__main__":

    t1 = ThreadWithReturnValue(target=square, args=(10,))
    t2 = ThreadWithReturnValue(target=cube, args=(10,))
    t1.start()
    t2.start()
    r1 = t1.join()
    r2 = t2.join()
    print(r1, t1._return, r2, t2._return)
