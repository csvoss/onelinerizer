def f():
    x = 1
    a = lambda: x
    b = (lambda: lambda: x)()
    c = (lambda: lambda: lambda: x)()()
    x = 2
    print a(), b(), c()
f()

def g():
    print [f() for f in [lambda: x for x in range(5)]]
    print [f() for f in [(lambda: lambda: x)() for x in range(5)]]
    print [f() for f in [(lambda x: lambda: x)(x) for x in range(5)]]
    print [f() for f in map(lambda x: lambda: x, range(5))]
g()
