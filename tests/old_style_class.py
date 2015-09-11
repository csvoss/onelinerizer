class C:
    def __getattr__(self, name):
        if name == '__str__':
            return lambda: 'foo'
        raise AttributeError
print C()

class D(C):
    pass
print D()
