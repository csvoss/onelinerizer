def g():
    x = 'outer'
    def h():
        x = 'inner'
        return x
    return (h(), x)
print g()
