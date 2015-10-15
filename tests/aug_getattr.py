class C:
    def __getattr__(self, name):
        global o
        if name == '__iadd__':
            o = None
        elif name == '__add__':
            return lambda other: None
        raise AttributeError

o = C()
o += 1
