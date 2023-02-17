
def outer():
	count = 0

	def inner(reset=False):
		nonlocal count
		if reset:
			count = 0
		count += 1
		print(f'{count} {"ole" * count}')
	return inner

# these each have their own copy of the count variable
ole = outer()
ole2 = outer()

del outer

ole()
ole()
ole()
ole(reset=True)
ole()

ole2()