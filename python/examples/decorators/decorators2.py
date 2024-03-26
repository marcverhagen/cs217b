# DECORATORS

# A decorator is a function that takes another function, then creates a new function
# that wraps around the other function and returns the new function.

def decorator(func):
    def wrapper():
        """The wrapper function created by the decorator function."""
        print("Actions before the wrapped function")
        func()
        print("Actions after the wrapped function")
    return wrapper


# Create a new function that we will wrap in the decorator

def say_whee():
    print("Whee!")

print()
print(decorator)
print(say_whee)

# Do the actual decoration

say_whee = decorator(say_whee)

print()
print(decorator)
print(say_whee)

print()
say_whee()
