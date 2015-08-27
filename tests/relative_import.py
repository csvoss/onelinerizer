__package__ = 'os'
import path
print path.join(*path.split('hello/world'))

__package__ = 'os.path'
from . import join
from ..path import split
print join(*split('hello/world'))

from .. import path
print path.join(*path.split('hello/world'))
