# user-defined errors


class IndustryError(Exception):
    pass


def keep_going():
	for i in range(10):
		print(f'going {i}')
	raise IndustryError('You stopped going')


try:
	keep_going()
except IndustryError as e:
	print('ERROR:', e)
