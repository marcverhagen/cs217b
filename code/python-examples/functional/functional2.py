# Introducing functional programming: map and filter


import math


print(list(map(str.upper, list('abcdef'))))
print(list(map(math.sqrt, (0, 1, 4, 9, 16, 25))))


def keep_worthy_numbers3(numbers: list, minimum_value: int):
    return list(map(lambda n: n if n > minimum_value else None, numbers))


def keep_worthy_numbers4(numbers: list, minimum_value: int):
    return list(filter(lambda n: n > minimum_value, numbers))


for fun in keep_worthy_numbers3, keep_worthy_numbers4:
    print(fun, fun([1, 2, 33, 12, 5, 78], 10))
