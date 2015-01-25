def print_decorator(f):
    def g(*args, **kwargs):
        print "The name of the function is",f.__name__
        return f(*args, **kwargs)
    return g

@print_decorator
def add_numbers(x,y):
    print x+y

add_numbers(42, 56)
