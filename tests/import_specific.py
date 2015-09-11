a = 0
b = 0
c = 0
_d = 0
__e = 0
print a, b, c, _d, __e

from tests.modules.with_all import a
print a, b, c, _d, __e

from tests.modules.without_all import b
print a, b, c, _d, __e
