import sys
import StringIO

print
print 1,
print 2

s = StringIO.StringIO()
print >>s, 3,
print >>s, 4
print repr(s.getvalue())

def f():
    print 'f'
    return sys.stdout
def g():
    print 'g'
    return 'hello'
print >>f(), g()
