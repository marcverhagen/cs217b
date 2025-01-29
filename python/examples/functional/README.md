# Functional programming morsels

This started with an example of "what's wrong with this code" where the doctor ordered a list comprehension (see [functional1.py](functional1.py)), but a student suggested that functional programming would be good too.

Python is not purely functional, but offers many functional elements. Functions are first class citizens and can for example be handed over as arguments to another function. Python also has the map, filter and reduce functions which all apply a function to elements of a list.

In [functional2.py](functional2.py) there are some simple map examples and an effort to use map and filter instead of a list comprehensions, as you will see the latter is a better fit.

Since lambda is a bit limited in Python you will often want a named function. There is a somewhat uneasy translation for this particular case because the original code had a function with two arguments, but the function used in map or filter should only have one argument. So in [functional3.py](functional3.py) we use inner and outer functions.

The latter reminded me of a closure so it could be enlighting to look at the closure example in [../closures](../closures/README.md).
