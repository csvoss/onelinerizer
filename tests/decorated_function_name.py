def decorator(f):
    print f.__name__
    def bar():
        return f()
    return bar

@decorator
def foo():
    pass
print foo.__name__
