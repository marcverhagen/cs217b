import package.a
import package.a as a_mod
from package import a
from package import b

print('<m:6>  package.a.DATA ', package.a.DATA)
print('<m:7>  a_mod.DATA     ', a_mod.DATA)
print('<m:8>  a.DATA         ', a.DATA)
print('<m:9>  b.a.DATA       ', b.a.DATA)
print('<m:10> b.DATA         ', b.DATA)
print('<m:11> package.DATA   ', package.DATA)
