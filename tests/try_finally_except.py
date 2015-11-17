try:
    try:
        print 'try 1'
        assert False
    finally:
        print 'finally 1'
except AssertionError:
    print 'except 1'
