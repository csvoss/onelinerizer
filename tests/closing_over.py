def f():
    x = 'closed-over'
    def g():
        return x
    return g
print f()()
