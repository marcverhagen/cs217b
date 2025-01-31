
class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]



class Class1(metaclass=Singleton): pass


class Class2(metaclass=Singleton): pass


# Creating instances
c1_instance1 = Class1()
c1_instance2 = Class1()
c2_instance1 = Class2()
c2_instance2 = Class2()


print()
print(id(c1_instance1), c1_instance1)
print(id(c1_instance2), c1_instance2)
print(c1_instance1 is c1_instance2)

print()
print(id(c2_instance1), c2_instance1)
print(id(c2_instance2), c2_instance2)
print(c2_instance1 is c2_instance2)
