# PASSING ARGUMENTS AND RETURNING VALUES

# Using the decorator in decorators3.py with a function that takes arguments
# causes an error. You need to hand them in the wrapper function.
#
# In the previous examples we also had the situation that the decorator basically
# swallows the value generated by the decorated function, if you want to return it
# you need to explicitly do that.

def argument_passing_decorator1(func):
    def wrapper(arg):
        return func(arg)
    return wrapper

@argument_passing_decorator1
def say(text: str):
    return text

print()
print(say('Hi'))


# Use the unpacking operator to hand in arbitrary arguments

def argument_passing_decorator2(func):
    def wrapper(*args, **kwargs):
        print('args   -->', args)
        print('kwargs -->', kwargs)
        return func(*args, **kwargs)
    return wrapper

@argument_passing_decorator2
def function_with_args(arg1, arg2, arg3=None, arg4=1):
    return(f'[{arg1}, {arg2}, {arg3}, {arg4}]')

print()
print(function_with_args(1, 2, arg3=4, arg4=5))
