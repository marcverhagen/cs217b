# STACKING DECORATORS

def square_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result ** 2
    return wrapper

def double_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 2
    return wrapper

@double_decorator
@square_decorator
def add(a, b):
    return a + b

result = add(2, 3)
print(result)