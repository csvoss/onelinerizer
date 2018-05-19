from __future__ import division
print eval('1/2')
exec('print 1/2')
eval(compile('print 1/2', 'wat.py', 'exec'))
print eval(compile('1/2', 'wat.py', 'eval'))
print eval(compile('1/2', 'wat.py', 'eval', 0, 0))
print eval(compile('1/2', 'wat.py', 'eval', 0, ~0))
