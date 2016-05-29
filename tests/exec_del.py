a = 0

def f():
    a = 1
    exec 'g = lambda: a; print a, g()'
    print a, g()
    exec 'a = 2; print a, g()'
    exec 'print a, g()'
    print a, g()
    exec 'del a; print a, g()'
    exec 'print a, g()'
    print a, g()
    a = 3
    exec 'print a, g()'
    print a, g()

f()

a = 4
exec 'g = lambda: a; print a, g()'
print a, g()
exec 'a = 5; print a, g()'
exec 'print a, g()'
print a, g()
exec 'del a; print a, g()'
exec 'print a, g()'
print a, g()
a = 6
exec 'print a, g()'
print a, g()
