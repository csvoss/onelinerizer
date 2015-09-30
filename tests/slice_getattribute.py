class M(type):
    __getattribute__ = None

class G(object):
    __metaclass__ = M
    __getattribute__ = None
    def __get__(self, instance, owner):
        def f(*args):
            print args
        return f

class C(object):
    __metaclass__ = M
    __getattribute__ = None
    __getitem__ = G()
    __setitem__ = G()
    __delitem__ = G()

o = C()
o.__getitem__ = None
o.__setitem__ = None
o.__delitem__ = None
o[:]
o[::]
o[:] = []
o[::] = []
del o[:]
del o[::]
