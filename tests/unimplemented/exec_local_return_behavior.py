def f():
    exec ""
    locals()['a'] = 6
    return a

def g():
    locals()['a'] = 6
    return a

a = 5
print f()

a = 5
print g()
