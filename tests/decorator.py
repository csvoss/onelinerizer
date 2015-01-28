def print_decorator(f):
    def g(*args, **kwargs):
        print "Calling the function!"
        return f(*args, **kwargs)
    return g

@print_decorator
def add_numbers(x,y):
    print x+y

add_numbers(42, 56)
