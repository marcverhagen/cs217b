"""

Using a dataclass combines the advantages of the named tuple with a few more bells
and whistles like being able use use type hints and th eposibility to initialize
with named arguments, at the cost of needing some more code.

"""

from dataclasses import dataclass

@dataclass
class Color:
	hue: float          # adding type hints
	saturation: float
	luminosity: float

# plus a more understandable way to initiate
p = Color(170, 0.1, 0.6)
p = Color(hue=170, saturation=0.1, luminosity=0.6)

print(p)
if p.saturation >= 0.5: 
	print("wow, that is bright")
if p.luminosity >= 0.5: 
	print("wow, that is light")