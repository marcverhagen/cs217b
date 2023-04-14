
DEBUG = False

# Context managers have in common that they set up some resource and then close it
# down after all work with the resource is done, even after something went wrong.

class File:

    """For a file setting up is opening it and closing is... closing it. You use the
    dunder methods (aka magic methods) __enter__ method and __exit__ to do that. When
    you add those methods you have created a context manager."""

    def __init__(self, file_name: str, method='r'):
        if DEBUG:
            print('>>> initializing...')
        self.name = file_name
        self.method = method

    def __str__(self):
        return f'<File name="{self.name}'

    def __enter__(self):
        # this happens after initialization, we just open the file and save the
        # file handle, which we return
        if DEBUG:
            print('>>> entering...')
        self.file = open(self.name, self.method)
        return self.file

    def __exit__(self, exception, message, traceback):
        # this will always run, unless an error occured above
        if DEBUG:
            print(f'>>> closing {self.name}')
        self.file.close()
        # when cleaning up you can also deal with errors
        if exception is ZeroDivisionError:
            print('Ignored zero division error')
            return True
        elif exception is not None:
            print('Other error, not ignoring it')
            print(exception, message)
            return False
