from pprint import pprint

class Human(type):
    def __new__(mcs, name, bases, class_dict):
        class_ = super().__new__(mcs, name, bases, class_dict)
        print('type.__new__', type.__new__)
        print('super.__new__', super().__new__)
        class_.species = 'homo sapiens'
        return class_


class Person(metaclass=Human):
    def __init__(self, name, age):
        self.name = name
        self.age = age

sue = Person('sue', 12)

print(type(Person))
print(type(sue))

print(object)
print(type(object))

print(Person.__dict__)
print(sue.__dict__)
print(sue.species)


class Hum:

    def __new__(cls, name):
        print('Hum             =', Hum)
        print('cls             =', cls)
        print('super           =', super)
        print('super()         =', super())
        print('super(Hum, cls) =', super(Hum, cls))
        #return super(cls).__new__(cls)
        return super().__new__(cls)
        return super(Hum, cls).__new__(cls)
        return Hum.super(cls).__new__(cls)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'<{self.__class__.__name__} "{self.name}">'

print()
print(Hum('me'))


def spam(self):
    return 'ham'

NewClass = type('NewClass', (), {'ham': 'ham', 'spam': spam})

print()
print(NewClass)
print(NewClass().spam())

def get_dir(inst):
    return [x for x in dir(inst) if not x.startswith('__')]

class Hum1:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f'<{self.__class__.__name__} {get_dir(self)}>'

class Hum2:
    def __new__(cls, name):
        print('1a. creating new instance, using', Hum1.__new__)
        inst = Hum1.__new__(Hum1)
        print('...', repr(inst), inst)
        print('1b. creating new instance, using', object.__new__)
        inst = object.__new__(Hum1)
        print('...', repr(inst), inst)
        print('2. initializing new instance, using', inst.__init__)
        inst.__init__(name)
        print('...', inst)
        return inst

class Hum3:
    def __new__(cls, name):
        inst = object.__new__(Hum1)
        inst.__init__(name)
        return inst

print()
eric = Hum2('eric')
sue = Hum3('sue')
print()
print(sue)


class New:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"New {self.name}"

print()
print(New('sue'))
obj = object.__new__(New, 'sue')
obj.__init__('sue')
print(obj)




##########

def debug_function(func):
    def wrapper(*args):
        print(f"{func.__qualname__}{args[1:]} --> {func(*args)}")
        return func(*args)
    return wrapper


def debug_all_methods(cls):
    print(cls)
    for key, val in vars(cls).items():
        print('kv', key,val)
        if callable(val):
            setattr(cls, key, debug_function(val))
    return cls


class MetaClassDebug(type):

    def __new__(cls, clsname, bases, clsdict):
        print('--', cls)
        print('--', clsname)
        print('--', bases)
        print('--', clsdict.keys())
        obj = super().__new__(cls, clsname, bases, clsdict)
        obj = debug_all_methods(obj)
        return obj


class Calc(metaclass=MetaClassDebug):

    def add(self, x, y):
        return x + y

    def sub(self, x, y):
        return x - y

    def mul(self, x, y):
        return x * y


calc = Calc()
calc.add(2, 3)
calc.sub(2, 3)
calc.mul(2, 3)

###############

# https://flexiple.com/python/metaprogramming-with-metaclasses-python

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MyClass(metaclass=SingletonMeta):
    pass

# Creating instances
instance1 = MyClass()
instance2 = MyClass()

# Output: True, demonstrating that both variables point to the same instance
print()
print(instance1 is instance2)

################


#https://www.pythontutorial.net/python-oop/python-metaclass/

from pprint import pprint


class Human2(type):
    def __new__(mcs, name, bases, class_dict, **kwargs):
        class_ = super().__new__(mcs, name, bases, class_dict)
        class_.species = "Homo sapiens"
        if kwargs:
            for name, value in kwargs.items():
                setattr(class_, name, value)
        return class_

class Person2(object, metaclass=Human2, country='USA'):
    def __init__(self, name, age):
        self.name = name
        self.age = age

print()
pprint(Person2.__dict__)
person = Person2("sue", 12)
pprint(person.__dict__)
print(person.species)
print(person.country)

