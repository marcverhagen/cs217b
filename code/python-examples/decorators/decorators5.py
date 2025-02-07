# INSPECTION

# One problem with the decorators is that it is hard to inspect the function
# that you are decorating. For example, if you want to print the function
# say_whee and its document string, what you get is the document string from
# the embedded function.

def decorator(func):
    def wrapper():
        """The wrapper function created by the decorator function."""
        func()
    return wrapper

@decorator
def say_whee():
    """Say whee, wrapped in a decorator."""
    print("Whee!")


print(f'\n{"="*80}\ndecorators5()\n{"="*80}\n')

print(say_whee)
print(say_whee.__doc__)


# So let's try that again. The functools module has functions that can be used as
# decorators and that give access to some aspects of the decorated function, for
# example the doc string to the wrapped function.

import functools

def decorator2(func):
    @functools.wraps(func)
    def wrapper():
        """The wrapper function created by the decorator function."""
        func()
    # Note: what is returned is the wrapper() function after it is decorated
    # by functools.wrap
    return wrapper

@decorator2
def say_whee2():
    """Say whee, wrapped in a decorator."""
    print('Whee!')

print()
print(say_whee2)
print(say_whee2.__doc__)
print()
