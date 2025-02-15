# HIGHER ORDER DECORATOR - part deux

# Remember that 
#
#     @decorator
#     def some_function(): ...
#
# is syntactic sugar for
#
#     def some_function(): ...
#     some_function = decorator(some_function)
#
# Backing away from the syntactic sugar may help see what is going on.


def log_decorator_with_prefix(prefix):
    def log_decorator(func):
        def wrapper(arg):
            print(f"{prefix} Executing '{func.__name__}({arg})'")
            func(arg)
        return wrapper
    return log_decorator

def say_hello(name):
    print(f"Hello, {name}")

print(f'\n{"="*80}\ndecorators6a()\n{"="*80}\n')


fun1 = log_decorator_with_prefix('[INFO]')
fun2 = fun1(say_hello)

print('>>>', fun1)
print('>>>', fun2)
fun2('Alice')


fun3 = log_decorator_with_prefix('[INFO]')(say_hello)

print('\n>>>', fun3)
fun3('Alice')
