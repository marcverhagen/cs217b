# Using named functions with map and filter


# This won't quite work because the function handed to map should only
# accept one argument.
def is_worthy(n: int, minimum_value: int):
    return n if n > minimum_value else None


# But this will. The outer function takes an number and then returns a function
# that compares another number to the first number.
def f(x):
    def g(y):
        return y if y > x else None
    return g


def keep_worthy_numbers5(numbers: list, minimum_value: int):
    return list(map(f(minimum_value), numbers))


def keep_worthy_numbers6(numbers: list, minimum_value: int):
    return list(filter(f(minimum_value), numbers))


for fun in keep_worthy_numbers5, keep_worthy_numbers6:
    print(fun, fun([1,2,33,12,5,78], 10))
