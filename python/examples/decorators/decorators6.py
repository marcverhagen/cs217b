# HIGHER ORDER FUNCTION

# The decorator can be given an argument. This is needed to make functools.wrap
# from decorators5.py work. It also explains what you see in Flask all the time:
#
# @app.get('/help')
# def help():
#     return "<p>Getting extremely minimal help via a GET request</p>"


def log_decorator_with_prefix(prefix):
    def log_decorator(func):
        def wrapper(*args, **kwargs):
            print(f"{prefix} Executing {func.__name__}")
            result = func(*args, **kwargs)
            return result
        return wrapper
    return log_decorator

@log_decorator_with_prefix("[INFO]")
def say_hello(name):
    print(f"Hello, {name}!")

print()
say_hello("Alice")


# The argument you hand into the decorator builder could be a function

def create_decorator_with(func1):
    def decorator(func2):
        def wrapper(numbers):
            print(func1)
            print(func2)
            print('decorator action -->', func1(numbers))
            func2(numbers)
        return wrapper
    return decorator

@create_decorator_with(min)
def print_list(numbers):
    #print(min(numbers))
    print('function action  -->', numbers)

print()
print_list([4,2,4,6,8,3,2])
