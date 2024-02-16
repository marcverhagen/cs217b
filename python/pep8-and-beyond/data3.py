"""

Using a dataclass combines the advantages of the named tuple with a few more bells
and whistles like being able to use type hints and the possibility to initialize
with named arguments, all at the small cost of some extra code.

"""

from dataclasses import dataclass

@dataclass
class Color:
	hue: float
	saturation: float
	luminosity: float

# a more understandable way to initiate
p = Color(170, 0.1, 0.6)
p = Color(hue=170, saturation=0.1, luminosity=0.6)

print(p)
if p.saturation >= 0.5: 
	print("wow, that is bright")
if p.luminosity >= 0.5: 
	print("wow, that is light")