try:
    print 'try 0'
finally:
    print 'finally 0'

def f():
    try:
        print 'try f'
    finally:
        print 'finally f'
    return 'returned'

print 'f: ' + f()

def g():
    try:
        print 'try g'
        return 'returned'
    finally:
        print 'finally g'

print 'g: ' + g()

def h():
    try:
        print 'try h'
    finally:
        print 'finally h'
        return 'returned'

print 'h: ' + h()

def i():
    try:
        print 'try i'
        return 'returned'
    finally:
        print 'finally i'
        return 'returned harder'

print 'i: ' + i()
