"""

Dealing with properties.

"""


class Horse:

    """The least effort, good for simple code. Just access the property directly."""

    def __init__(self, breed):
        self.breed = breed


print('*** Testing horse code\n')
secretariat = Horse('Arabian')
print(secretariat.breed)
secretariat.breed = 'American Belgian Draft'
print(secretariat.breed)


class Dog:

    """User getters and setters was popular. The advantage is that you can
    add some code in the methods to do some computation if needed for a getter,
    or do some validation with setters. Big disadvantage if you intoduce this
    later is that you need to track down the cases where you used properties
    directly. Also, you now have two ways of accessing properties. Also, this 
    is not the most Pythonic way."""

    def __init__(self, breed):
        self.breed = breed

    def get_breed(self):
        return self.breed

    def set_breed(self, breed):
        self.breed = breed


print('\n*** Testing dog code\n')
fluffy = Dog(breed='rotweiler')
print(fluffy.get_breed())
fluffy.set_breed('puppy')
print(fluffy.get_breed())


class Cat:

    """Best way is to use properties. You can still use code in the methods for
    computation and validation, but you still use the same simple mechanism for
    all access. You could of course go directly to the _breed variable, but you
    know you should not do that because the leading underscore indicates that
    _breed is supposed to be private."""

    def __init__(self, value):
        # introduce a "private" variable for the raw storage
        self._breed = value

    @property
    def breed(self):
        return self._breed

    @breed.setter
    def breed(self, value):
        self._breed = value

 
print('\n*** Testing cat code\n')
tommy = Cat('tomcat')
print(tommy.breed)
tommy.breed = 'abyssinian'
print(tommy.breed)
