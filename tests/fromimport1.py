from os import path
print(path.join.__name__)
from os.path import join
print(join.__name__)
from os import path as path_aliased
print(path_aliased.join.__name__)
from os.path import join as join_aliased
print(join_aliased.__name__)
from os.path import abspath, realpath as realpath_aliased
print(abspath.__name__)
print(realpath_aliased.__name__)
# TODO: how to test explicit relative import `from . import bar` `from .. import bar`
