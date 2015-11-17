try:
    print 'try 0'
except AssertionError:
    print 'except 0'
else:
    print 'else 0'

try:
    print 'try 1'
    assert False
except AssertionError:
    print 'except 1'
else:
    print 'else 1'

try:
    try:
        print 'try 2'
        assert False
    except ZeroDivisionError:
        print 'wrong except 2'
    else:
        print 'else 2'
except AssertionError:
    print 'right except 2'
else:
    print 'else 2'

try:
    print 'try 3'
    assert False
except ZeroDivisionError:
    print 'wrong except 3'
except AssertionError:
    print 'right except 3'
else:
    print 'else 3'

try:
    print 'try 4'
    assert False
except:
    print 'except 4'
else:
    print 'else 4'

def f():
    try:
        print 'try f'
        return 'returned'
    except AssertionError:
        print 'except f'
    else:
        print 'else f'

print 'f: ' + f()

def g():
    try:
        print 'try g'
        assert False
    except AssertionError:
        print 'except g'
        return 'returned'
    else:
        print 'else g'

print 'g: ' + g()

def f():
    try:
        print 'try h'
    except:
        print 'except h'
    else:
        print 'else h'
        return 'returned'

print 'h: ' + f()
