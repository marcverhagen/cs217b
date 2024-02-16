"""

Using a named tuple instantly makes the code from data1.py more readable.

"""

from collections import namedtuple

Color = namedtuple('Color', ['hue', 'saturation', 'luminosity'])

p = Color(170, 0.1, 0.6)

print(p)
if p.saturation >= 0.5: 
	print("wow, that is bright")
if p.luminosity >= 0.5: 
	print("wow, that is light")
