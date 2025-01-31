
def keep_worthy_numbers(numbers, minimum_value):
    result = []
    for number in numbers:
        if number > minimum_value:
            result.append(number)
    return result


def keep_worthy_numbers2(numbers: list, minimum_value: int):
	return [n for n in numbers if n > minimum_value]


print(keep_worthy_numbers([1,2,33,12,5,78], 10))
print(keep_worthy_numbers2([1,2,33,12,5,78], 10))