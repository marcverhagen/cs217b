# The simplest metaclass

class Human:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class newtype(type):
    pass

class NewHuman(metaclass=newtype):
    pass

class NewHuman(Human, metaclass=newtype):
    pass


print('type(newtype)                 --> ', type(newtype))
print('newtype.__bases__             --> ', newtype.__bases__)
print('type(NewHuman)                --> ', type(NewHuman))
print('NewHuman.__bases__            --> ', NewHuman.__bases__)
print('isinstance(newtype, object)   --> ', isinstance(newtype, object))
print('isinstance(newtype, type)     --> ', isinstance(newtype, type))
print('isinstance(NewHuman, object)  --> ', isinstance(NewHuman, object))
print('isinstance(NewHuman, type)    --> ', isinstance(NewHuman, type))