def function_call(x, y, *args, **kwargs):
    print x,y,args,kwargs

function_call(42, "stringy\n\"", 5, 6, 7, foo=43+4, bar=22)
