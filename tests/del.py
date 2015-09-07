i = 17
del i

class dummy(object):
    def __init__(self):
        self.foo = 1
        print getattr(self, 'foo', 'missing')
        del self.foo
        print getattr(self, 'foo', 'missing')

dummy()

a = range(15)
del (a[4:6], [a[::2], a[4]]), a[0]
print a

del []
del [], []
