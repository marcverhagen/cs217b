import inspect
from itertools import combinations

class newtype(type): pass
class Human: pass
class NewHuman(Human, metaclass=newtype): pass
sue = Human()
newsue = NewHuman()


objects = (
	('object', object),
	('type', type),
	('newtype', newtype),
	#('Human', Human),
	('NewHuman', NewHuman),
	#('sue', sue),
	('newsue', newsue),
	#('int', int),
	#('object()', object()),
	#('newint', type('newint', (type,), {})),
	#('100', 100)
)

pairs = list(combinations(objects, 2))


def is_subclass(o1, o2):
	if inspect.isclass(o1) and inspect.isclass(o2):
		return o2 in o1.__bases__
	else:
		return None

def is_instance(o1 ,o2):
	if inspect.isclass(o2):
		return isinstance(o1,o2)
	else:
		return None


#'''
print()
for (n1, o1), (n2, o2) in pairs:
	print()
	print(f'is-subclass({n1}, {n2}) ==>  {is_subclass(o1, o2)}')
	print(f'is-instance({n1}, {n2}) ==>  {is_instance(o1, o2)}')
	print(f'is-subclass({n2}, {n1}) ==>  {is_subclass(o2, o1)}')
	print(f'is-instance({n2}, {n1}) ==>  {is_instance(o2, o1)}')
#'''

print()
for (n1, o1), (n2, o2) in pairs:
	if is_instance(o1, o2):
		header = f"is-instance({n1}, {n2})"
		print(f'{header:30} ==>  {is_instance(o1, o2)}')
	if is_instance(o2, o1):
		header = f"is-instance({n2}, {n1})"
		print(f'{header:30} ==>  {is_instance(o2, o1)}')

print()
for (n1, o1), (n2, o2) in pairs:
	if is_subclass(o1, o2):
		header = f"is-subclass({n1}, {n2})"
		print(f'{header:30} ==>  {is_subclass(o1, o2)}')
	if is_subclass(o2, o1):
		header = f"is-subclass({n2}, {n1})"
		print(f'{header:30} ==>  {is_subclass(o2, o1)}')

print()
for name, obj in objects:
	if is_subclass(obj, obj):
		header = f"is-subclass({name}, {name})"
		print(f'{header:30} ==>  {is_subclass(obj, obj)}')
	if is_instance(obj, obj):
		header = f"is-instance({name}, {name})"
		print(f'{header:30} ==>  {is_instance(obj, obj)}')
	