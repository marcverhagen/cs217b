# STACKING DECORATORS

def double(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 2
    return wrapper

def triple(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 3
    return wrapper

@double
@triple
def add(a, b):
    return a + b

result = add(2, 3)


print(f'\n{"="*80}\ndecorators7()\n{"="*80}\n')

print(result)
print()