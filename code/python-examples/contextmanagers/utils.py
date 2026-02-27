
# Context managers have in common that they set up some resource and then close it
# down after all work with the resource is done, even after something went wrong.

class File:

    """For a file setting up is opening it and closing is... closing it. You use the
    dunder methods (aka magic methods) __enter__ method and __exit__ to do that. When
    you add those methods you have created a context manager."""

    def __init__(self, file_name: str, debug=False, method='r'):
        # For initialization we typically store some information relevant to the 
        # resource, like the file name for example.
        if debug:
            print('--- initializing...')
        self.debug = debug
        self.name = file_name
        self.method = method

    def __str__(self):
        return f'<File name="{self.name}'

    def __enter__(self):
        # This happens after initialization, we just open the file and save the
        # file handle, which we return.
        if self.debug:
            print('--- entering...')
        self.fh = open(self.name, self.method)
        return self.fh

    def __exit__(self, exception, message, traceback):
        # This will always run, unless an error occured in __init__ or __enter__.
        if self.debug:
            print('--- closing...')
        self.fh.close()
        # When cleaning up you can also deal with errors
        if exception is ZeroDivisionError:
            # dealing with the error and returning True
            print('--- ignoring zero division error...')
            return True
        if exception is FileNotFoundError:
            # We know about this error, but we don't want to trap it, returning False raises
            # the error again.
            print('--- file not found, exiting with an error...')
            print('---', exception, message)
            return False
        elif exception is not None:
            # And all the other possible problems, let's say we just want to alert is to them
            # but not break the script.
            print('--- other error, ignoring it, but reportinh...')
            print('---', exception, message)
            return True