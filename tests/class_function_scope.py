def f(x, y):
    print x
    print y
    class c:
        x = 4
        print x
        print y
        def g(self):
            print x
            print y
            print c
    return c
print f("x", "y")().g()
