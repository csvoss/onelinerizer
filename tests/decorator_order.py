def f0(g0):
    print 0
    return lambda: [0] + g0()

def f1(g1):
    print 1
    return lambda: [1] + g1()

@f0
@f1
def g():
    print 2
    return [2]

print g()
