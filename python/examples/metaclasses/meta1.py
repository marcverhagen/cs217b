class Human:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'

print(Human('sue'))


class Human(object, metaclass=type):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'

print(Human('sue'))
print(type(Human('sue')))
