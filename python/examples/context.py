# context managers


# You probably have used context managers before.

fname = 'context.py'
with open(fname) as fh:
    print(f'Line 1 of {fname}: {fh.readlines()[0]}')


# What sits behind that is a class (typically) with an __enter__ method and an
# __exit__ method. The former sets up the context and the latter cleans up after 
# we exit the context, it does that even if an exception was raised.

class File:

    def __init__(self, file_name: str, method='r'):
        print('>>> initializing...')
        self.name = file_name
        self.method = method

    def __str__(self):
        return f'<File name="{self.name}'

    def __enter__(self):
        # this happens after initialization, we just open the file and save the
        # file handle, which we return
        print('>>> entering...')
        self.file = open(self.name, self.method)
        return self.file

    def __exit__(self, exception, message, traceback):
        # when cleaning up you can also deal with errors
        if exception == ZeroDivisionError:
            print('Ignored zero division error')
        elif exception is not None:
            print('Other error, not dealing with it though')
            print(exception, message)
        # this will always run, unless an error occured above
        print(f'>>> closing {self.name}')
        self.file.close()
        return True


# this is pretty much the same as lines 7-8
with File(fname) as fh:
    print(fh.readlines()[0])

# now we introduce an error, which will be caught
with File(fname) as fh:
    open('xxx')
