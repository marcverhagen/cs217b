import package.a
import package.a as a_mod
from package import a
from package import b

print(package.a.DATA)
print(a_mod.DATA)
print(a.DATA)
print(b.a.DATA)
print(b.DATA)
