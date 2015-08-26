# Test by andersk
## The issue here is that when we modify y, we also instantiate a new y...
x = [1]
y = x
y += [2]
print x
