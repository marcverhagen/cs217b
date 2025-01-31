# SYNTACTIC SUGAR

# With the code in decorators2.py we use the name "say_whee" three times (function
# definition, embedding in the decorator and reassigning to the variable). We can
# use the pie syntax as syntactic sugar and use the name "say_whee" only when we 
# define the "say whee" function. (By the way, it is called pie syntax because
# some think the @ symbol looks like a pie).

def decorator(func):
    def wrapper():
        """The wrapper function created by the decorator function."""
        print("Actions before the wrapped function")
        func()
        print("Actions after the wrapped function")
    return wrapper

# "@decorator" is just a short way of saying "say_whee = decorator(say_whee)""

@decorator
def say_whee():
    """Say whee, but wrap a decorator around it."""
    print("Whee!")


print()
print(decorator)
print(say_whee)

print()
say_whee()
