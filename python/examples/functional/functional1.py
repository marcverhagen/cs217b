# From the "What's wrong" slides

def keep_worthy_numbers1(numbers, minimum_value):
    result = []
    for number in numbers:
        if number > minimum_value:
            result.append(number)
    return result

def keep_worthy_numbers2(numbers: list, minimum_value: int):
	return [n for n in numbers if n > minimum_value]
