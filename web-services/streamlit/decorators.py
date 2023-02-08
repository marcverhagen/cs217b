"""
https://pythonbasics.org/decorators/
"""

def hello(func):
    def inner(name: str):
        print(f"Hello")
        func(name)
    return inner

def print_name1(name: str):
    print(name)

wrapped_function = hello(print_name1)
wrapped_function('Jane')

@hello
def print_name2(name: str):
    print(name)

print_name2('Sue')
