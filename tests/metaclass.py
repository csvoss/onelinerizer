class M(type):
    def __init__(cls, name, bases, dct):
        print 'metaclass'
        super(M, cls).__init__(name, bases, dct)

class C:
    __metaclass__ = M

class C(object):
    __metaclass__ = M

__metaclass__ = M

class C:
     pass
