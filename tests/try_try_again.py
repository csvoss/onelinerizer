def f():
    try:
        try:
            return 'returned'
        except AssertionError:
            pass
    except AssertionError:
        pass

print 'f: ' + f()
