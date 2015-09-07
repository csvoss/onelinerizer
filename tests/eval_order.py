import sys

def trace(msg, value):
    print msg
    return value

@trace('function decorator 0', lambda f: f)
@trace('function decorator 1', lambda f: f)
def function_def(
        arg0=trace('function default 0', None),
        arg1=trace('function default 1', None)):
    trace('function body', None)

class base0: pass
class base1: pass

@trace('class decorator 0', lambda cls: cls)
@trace('class decorator 1', lambda cls: cls)
class class_def(trace('class base 0', base0), trace('class base 1', base1)):
    trace('class body', None)

o = base0()
o.attr0 = o.attr1 = o.attr2 = o.attr3 = o.attr4 = 0
l = [0, 0]
d = {(0, 0): 0, (1, 1): 1}

del trace('del value 0', o).attr0, \
    trace('del value 1', l)[trace('del index', 0)], \
    trace('del value 2', l)[trace('del lower', 0):trace('del upper', 0):trace('del step', 1)], \
    trace('del value 3', d)[trace('del index 0', 0), trace('del index 1', 0)], \
    [trace('del value 4', o).attr1, trace('del value 5', o).attr2], \
    (trace('del value 6', o).attr3, trace('del value 7', o).attr4)

trace('assign target 0', o).attr, trace('assign target 1', o).attr = \
    trace('assign target 2', o).attr, trace('assign target 3', o).attr = \
    trace('assign value', (0, 0))
trace('aug assign target 0', o).attr += trace('aug assign value 0', 0)
trace('aug assign target 1', l)[trace('aug assign index', 0)] += trace('aug assign value 1', 0)
trace('aug assign target 2', l)[trace('aug assign lower 2', 0):trace('aug assign upper 2', 0)] += trace('aug assign value 2', [])
trace('aug assign target 3', l)[trace('aug assign lower 3', 0):trace('aug assign upper 3', 0):trace('aug assign step 3', 1)] += trace('aug assign value 2', [])

print >>trace('print file', sys.stdout), trace('print arg', 0)

for trace('for target', o).attr in trace('for iter', [0]):
    trace('for body', None)
else:
    trace('for else', None)

b = True
while trace('while test', b):
    trace('while body', None)
    b = False
else:
    trace('while else', None)

for b in [True, False]:
    if trace('if test', b):
        trace('if body', None)
    else:
        trace('if orelse', None)

# TODO: with

# TODO: raise

# TODO: try

assert trace('assert test', True), trace('assert message', '')

exec trace('exec body', '')
exec trace('exec body', '') in trace('exec globals', {})
exec trace('exec body', '') in trace('exec globals', {}), trace('exec locals', {})

trace('bool op left', True) or trace('bool op right', True)
trace('bin op left', 0) + trace('bin op right', 0)
not trace('unary op operand', True)
lam = lambda lambda_arg0=trace('lambda default 0', None), \
    lambda_arg1=trace('lambda default 1', None), \
    *lambda_args, **lambda_kwargs: \
    trace('lambda body', None)
for b in [True, False]:
    trace('if exp body', None) if trace('if exp test', b) else trace('if exp orelse', None)
{trace('dict key 0', 0): trace('dict value 0', 0), trace('dict key 1', 1): trace('dict value 1', 1)}
{trace('set elt 0', 0), trace('set elt 1', 1)}

[trace('list comp elt', 0)
 for trace('list comp target 0', o).attr in trace('list comp iter 0', [0])
 if trace('list comp test 0', True) if trace('list comp test 1', True)
 for trace('list comp target 1', o).attr in trace('list comp iter 1', [0])
 if trace('list comp test 2', True) if trace('list comp test 3', True)]

{trace('set comp elt', 0)
 for trace('set comp target 0', o).attr in trace('set comp iter 0', [0])
 if trace('set comp test 0', True) if trace('set comp test 1', True)
 for trace('set comp target 1', o).attr in trace('set comp iter 1', [0])
 if trace('set comp test 2', True) if trace('set comp test 3', True)}

{trace('dict comp key', 0): trace('dict comp value', 0)
 for trace('dict comp target 0', o).attr in trace('dict comp iter 0', [0])
 if trace('dict comp test 0', True) if trace('dict comp test 1', True)
 for trace('dict comp target 1', o).attr in trace('dict comp iter 1', [0])
 if trace('dict comp test 2', True) if trace('dict comp test 3', True)}

next(trace('generator exp elt', 0)
     for trace('generator exp target 0', o).attr in trace('generator exp iter 0', [0])
     if trace('generator exp test 0', True) if trace('generator exp test 1', True)
     for trace('generator exp target 1', o).attr in trace('generator exp iter 1', [0])
     if trace('generator exp test 2', True) if trace('generator exp test 3', True))

# TODO: yield

trace('compare left', 0) < trace('compare middle', 1) < trace('compare right', 2)

trace('lambda func', lam)(
    trace('lambda arg 0', 0),
    trace('lambda arg 1', 1),
    kwarg=trace('lambda kwarg', 0),
    *trace('lambda args', []),
    **trace('lambda kwargs', {}))

`trace('repr value', 0)`

trace('attribute value', o).attr
trace('slice2 value', l)[trace('slice2 lower', 0):trace('slice2 upper', 0)]
trace('slice3 value', l)[trace('slice3 lower', 0):trace('slice3 upper', 0):trace('slice3 step', 1)]
trace('subscript value', l)[trace('subscript index', 0)]
trace('extslice value', d)[trace('extslice index 0', 1), trace('extslice index 1', 1)]

[trace('list elt 0', 0), trace('list elt 1', 1)]
(trace('tuple elt 0', 0), trace('tuple elt 1', 1))
