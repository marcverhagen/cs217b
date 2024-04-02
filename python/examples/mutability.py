# Mutable classes in dictionaries

# Here is a mutuble class that can be added to a set because it has a __hash__
# method. According to the Python documentation it should also have a __eq__,
# method, which sure makes sense, but it is technically not needed.

class Thing():

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<Thing name=%s hash=%s>" \
			% (self.name, hash(self))

    def __hash__(self):
        return hash(self.name)

# Now you can create a set and add instances of this mutable type

s = set()
t1 = Thing(1)
t2 = Thing(2)
s.add(t1)
s.add(t2)
print(s)

# One thing to keep track of though is that you should not change the name variable:

t1 in s        # returns True
t1.name = 3
t1 in s        # returns False
