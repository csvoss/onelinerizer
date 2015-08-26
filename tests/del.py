i = 17
del i

o = type('dummy', (), {})()
o.foo = 1
print getattr(o, 'foo', 'missing')
del o.foo
print getattr(o, 'foo', 'missing')

a = range(15)
del (a[4:6], [a[::2], a[4]]), a[0]
print a
