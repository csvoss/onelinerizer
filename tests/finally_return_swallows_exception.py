def f():
    try:
        print 'try f'
        assert False
    finally:
        print 'finally f'
        return 'returned'

print 'f: ' + f()
