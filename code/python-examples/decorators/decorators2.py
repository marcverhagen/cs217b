# DECORATORS

# A decorator is a function that takes another function as an argument, then creates
# a new function that wraps around the argument function and returns the new function.

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


# And decorate it

decorated_say_whee = decorator(say_whee)


print(f'\n{"="*80}\ndecorators2()\n{"="*80}\n')

print(decorator)
print(say_whee)
print(decorated_say_whee)

print()
say_whee()
print()
decorated_say_whee()
print()