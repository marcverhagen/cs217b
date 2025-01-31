
from pprint import pprint


class HumanType(type):

    def __new__(mcs, name, bases, class_dict):
        class_ = super().__new__(mcs, name, bases, class_dict)
        class_.species = "Homo sapiens"
        return class_


class Person(object, metaclass=HumanType):

    def __init__(self, name):
        self.name = name

    def __str__(self):
    	return f'<{self.species} - {self.name}>'


print()
pprint(Person.__dict__)
print()
sue = Person('sue')
print(sue)
pprint(sue.__dict__)
