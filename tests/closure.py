a = 1
print a
def outer(b):
    c = 3
    print a, b, c
    def inner(d):
        e = 5
        print a, b, c, d, e
        return lambda f: (a, b, c, d, e, f)
    return inner
print outer(2)(4)(6)
