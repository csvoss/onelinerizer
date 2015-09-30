import types

def trace(name):
    def f(self, *args):
        print name, repr(args)
        return 0
    return f

def get(a, s):
    a[1*s]
    a[...]
    a[:]
    a[2*s:]
    a[:3*s]
    a[4*s:5*s]
    a[::]
    a[6*s::]
    a[:7*s:]
    a[::8*s]
    a[9*s:10*s:]
    a[11*s::12*s]
    a[:13*s:14*s]
    a[15*s:16*s:17*s]
    a[18*s, 19*s:20*s, 21*s:22*s:23*s, :, ::, ...]
    a[24*s,]
    a[25*s:26*s,]
    a[27*s:28*s:29*s,]
    a[...,]
    a[:,]
    a[::,]

def set(a, s):
    a[1*s] = 0
    a[...] = 0
    a[:] = 0
    a[2*s:] = 0
    a[:3*s] = 0
    a[4*s:5*s] = 0
    a[::] = 0
    a[6*s::] = 0
    a[:7*s:] = 0
    a[::8*s] = 0
    a[9*s:10*s:] = 0
    a[11*s::12*s] = 0
    a[:13*s:14*s] = 0
    a[15*s:16*s:17*s] = 0
    a[18*s, 19*s:20*s, 21*s:22*s:23*s, :, ::, ...] = 0
    a[24*s,] = 0
    a[25*s:26*s,] = 0
    a[27*s:28*s:29*s,] = 0
    a[...,] = 0
    a[:,] = 0
    a[::,] = 0

def aug(a, s):
    a[1*s] += 0
    a[...] += 0
    a[:] += 0
    a[2*s:] += 0
    a[:3*s] += 0
    a[4*s:5*s] += 0
    a[::] += 0
    a[6*s::] += 0
    a[:7*s:] += 0
    a[::8*s] += 0
    a[9*s:10*s:] += 0
    a[11*s::12*s] += 0
    a[:13*s:14*s] += 0
    a[15*s:16*s:17*s] += 0
    a[18*s, 19*s:20*s, 21*s:22*s:23*s, :, ::, ...] += 0
    a[24*s,] += 0
    a[25*s:26*s,] += 0
    a[27*s:28*s:29*s,] += 0
    a[...,] += 0
    a[:,] += 0
    a[::,] += 0

def delete(a, s):
    del a[1*s]
    del a[...]
    del a[:]
    del a[2*s:]
    del a[:3*s]
    del a[4*s:5*s]
    del a[::]
    del a[6*s::]
    del a[:7*s:]
    del a[::8*s]
    del a[9*s:10*s:]
    del a[11*s::12*s]
    del a[:13*s:14*s]
    del a[15*s:16*s:17*s]
    del a[18*s, 19*s:20*s, 21*s:22*s:23*s, :, ::, ...]
    del a[24*s,]
    del a[25*s:26*s,]
    del a[27*s:28*s:29*s,]
    del a[...,]
    del a[:,]
    del a[::,]

def g(e):
    def __getattr__(self, name):
        print '__getattr__', repr(name)
        if name == '__len__':
            return lambda: 100
        if name in e:
            return e[name].__get__(self)
        raise AttributeError
    return {'__getattr__': __getattr__}

for ns in [['__%sitem__'], ['__%sitem__', '__%sslice__']]:
    e = {n % a: trace(n % a) for a in ['get', 'set', 'del'] for n in ns}
    for meta, d in [
            (type, e),
            (type, dict(e, __len__=lambda self: 100)),
            (types.ClassType, dict(e, __len__=lambda self: 100)),
            (types.ClassType, g(e))]:
        a = meta('dummy', (), d)()
        for s in [1, -1]:
            get(a, s)
            set(a, s)
            aug(a, s)
            delete(a, s)
