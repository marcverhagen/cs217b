# You have an outer function that has a local variable and that defines
# and returns an inner function that refers to the variable, that variable
# will now preserve its state.

def outer():
	count = 0
	def inner(reset=False):
		nonlocal count
		if reset:
			count = 0
		count += 1
		print(f'count={count}')
	return inner


# These each have their own copy of the count variable.
ole = outer()
hoppa = outer()


# Don't need this anymore so you could even delete it if you want.
del outer


# Now we just call those two functions
ole()
ole()
ole()
ole(reset=True)
ole()
hoppa()
hoppa()
