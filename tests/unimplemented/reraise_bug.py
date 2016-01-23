# https://bugs.python.org/issue23556

try:
    try:
        raise Exception('foo')
    except Exception:
        try:
            raise Exception('bar')
        except Exception:
            pass

        # In Python 3, this reraises the caught Exception('foo'), like
        # you'd expect.  In Python 2, this reraises the ignored
        # Exception('bar').
        raise

except Exception as e:
    print(repr(e))

try:
    try:
        raise Exception('foo')
    except Exception:
        def f():
            try:
                raise Exception('bar')
            except Exception:
                pass
        f()

        # If we move the inner exception handler into a function, we
        # get the expected Exception('foo') in all versions.
        raise

except Exception as e:
    print(repr(e))
