# FUNCTIONS IN FUNCTIONS

# Functions are first class objects that can be handed in to other functions

def say_hello(name):
    return f"Hello {name}"

def say_bye(name):
    return f"Bye {name}"

def greet(name, greeter_func):
    return greeter_func(name)

print()
print(greet('Bob', say_hello))
print(greet('Bob', say_bye))


# You can define functions inside of other functions. These inner functions aren’t
# defined until the parent function is called. They’re locally scoped to parent(),
# meaning they only exist inside the parent() function as local variables. 

def parent():
    def first_child():
        print("Printing from first_child()")
    def second_child():
        print("Printing from second_child()")
    print("Printing from parent()")
    second_child()
    first_child()

print()
parent()


# You can return a function object from a function

def parent():
    print("Turning a parent function into a child function")
    def child():
        print("Running child function")
    return child

print()
fun = parent()
print(fun)
fun()
