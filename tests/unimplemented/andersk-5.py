# Test by andersk
f = lambda: 1
g = lambda x=f(): x
print g()
