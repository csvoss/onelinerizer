import ast
import sys


## TODO: Detect which features are ACTUALLY needed, and modify the code accordingly.

## Need __d and the list comprehension trick if we do anything involving __d -- while, for, if
## Need __print if we print
## Need __y if we use while
## Need __builtin__ if we use __print OR if we use __d


## Typesetting abstractions


DUNDER_PRINT = "__print"
DUNDER_EXEC = "__exec"
DUNDER_Y = "__y"
DUNDER_D = "__d"

COMMA = ", "
CONTINUATION = "%s"

def lambda_function(arguments_to_values, prettyprinted=False):
    ## arguments_to_values :: {argument_i: value_i}
    ## :: string
    if prettyprinted:
        raise NotImplementedError
    else:
        return "(lambda " + COMMA.join(arguments_to_values.keys()).replace("%", "%%") + ": " + CONTINUATION + ")(" + COMMA.join(arguments_to_values.values()).replace("%", "%%") + ")"


### Actual logicky code begins here


def get_init_code(tree):
    ## Return a string with %s somewhere in.
    ## INIT_CODE = "(lambda __builtin__: (lambda __print, __y, __d: %s)(__builtin__.__dict__['print'],(lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))),type('StateDict',(),__builtin__.__dict__)()))(__import__('__builtin__'))"

    ## TODO: Short-circuit to something far simpler if the program has but one print statement.

    need_print = True ## true if prints anywhere. TODO.
    need_exec = True ## true if execs anywhere. TODO.
    need_y_combinator = True ## true if uses a while. TODO.
    need_state_dict = True ## true if uses anything involving __d -- while, for, if. Also governs the list comprehension trick. TODO.
    need_dunderbuiltin = need_print or need_state_dict
    need_sys = True ## true if anything uses raise with no arguments, del a[:], or del a[n:]. TODO.

    output = "%s"
    if need_dunderbuiltin:
        output = output % lambda_function({"__builtin__": "__import__('__builtin__')"})

    arguments = {}
    if need_print:
        arguments[DUNDER_PRINT] = "__builtin__.__dict__['print']"
    if need_exec:
        arguments[DUNDER_EXEC] = "__import__('trace').Trace(count=False, trace=False).runctx"
    if need_y_combinator:
        arguments[DUNDER_Y] = "(lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args))))"
    if need_state_dict:
        arguments[DUNDER_D] = "type('StateDict',(),__builtin__.__dict__)()"
    if need_sys:
        arguments['sys'] = "__import__('sys')"

    if len(arguments.keys()) > 0:
        output = output % lambda_function(arguments)

    return output
        



## Parsing begins here


def fields(tree):
    return dict(list(ast.iter_fields(tree)))

def child_nodes(tree):
    return list(ast.iter_child_nodes(tree))

def many_to_one(trees, after='None'):
    # trees :: [Tree]
    # return :: string
    assert type(trees) is list
    if len(trees) is 0:
        return after
    else:
        return code_with_after(trees[0], many_to_one(trees[1:], after=after))

def code(tree):
    return code_with_after(tree, 'None')


def assignment_component(after, targets, value):
    ## return "(lambda %s: %s)(%s)" % (targets, after, value)
    return '[%s for %s in [(%s)]][0]' % (after, targets, value)


def slice_repr(slice):
    if type(slice) is ast.Ellipsis:
        return 'Ellipsis'
    elif type(slice) is ast.Slice:
        return 'slice(%s, %s, %s)' % (
            'None' if slice.lower is None else code(slice.lower),
            'None' if slice.upper is None else code(slice.upper),
            'None' if slice.step is None else code(slice.step))
    elif type(slice) is ast.ExtSlice:
        return '(%s)' % ' '.join(slice_repr(dim) + ',' for dim in slice.dims)
    elif type(slice) is ast.Index:
        return code(slice.value)
    else:
        raise NotImplementedError('Case not caught: %s' % str(type(slice)))

def delete_code(target):
    if type(target) is ast.Attribute:
        return 'delattr(%s, %r)' % (code(target.value), target.attr)
    elif type(target) is ast.Subscript:
        if type(target.slice) is ast.Slice and target.slice.step is None:
            return lambda_function({'__value': code(target.value)}) % \
                ("getattr(__value, '__delslice__', lambda __lower, __upper: __value.__delitem__(slice(%s, %s)))(%s, %s)" % \
                 ('None' if target.slice.lower is None else '__lower',
                  'None' if target.slice.upper is None else '__upper',
                  '0' if target.slice.lower is None else code(target.slice.lower),
                  'sys.maxint' if target.slice.upper is None else code(target.slice.upper)))
        else:
            return '%s.__delitem__(%s)' % (code(target.value), slice_repr(target.slice))
    elif type(target) is ast.Name:
        return 'delattr(__d, %r)' % target.id
    elif type(target) in (ast.List, ast.Tuple):
        return ', '.join(map(delete_code, target.elts))
    else:
        raise NotImplementedError('Case not caught: %s' % str(type(target)))

def code_with_after(tree, after):
    if type(tree) is ast.Add:
        return '+'
    elif type(tree) is ast.And:
        return ' and '
    elif type(tree) is ast.Assert:
        return '(%s if %s else ([] for [] in []).throw(AssertionError%s))' % (
            after, code(tree.test), '' if tree.msg is None else '(%s)' % code(tree.msg))
    elif type(tree) is ast.Assign:
        targets = [code(target) for target in tree.targets]
        value = code(tree.value)
        targets = ','.join(targets)
        return assignment_component(after, targets, value if len(tree.targets) == 1 else '[%s]*%d' % (value, len(tree.targets)))
    elif type(tree) is ast.Attribute:
        return '%s.%s' % (code(tree.value), tree.attr)
    elif type(tree) is ast.AugAssign:
        target = code(tree.target)
        op = code(tree.op)
        iop = type(tree.op).__name__.lower()
        if iop.startswith('bit'):
            iop = iop[len('bit'):]
        iop = '__i%s__' % iop
        value = code(tree.value)
        value = '(lambda __target, __value: (lambda __ret: __target %s __value if __ret is NotImplemented else __ret)(getattr(__target, %r, lambda other: NotImplemented)(__value)))(%s, %s)' % (op, iop, target, value)
        return assignment_component(after, target, value)
    elif type(tree) is ast.BinOp:
        return '(%s%s%s)' % (code(tree.left), code(tree.op), code(tree.right))
    elif type(tree) is ast.BitAnd:
        return '&'
    elif type(tree) is ast.BitOr:
        return '|'
    elif type(tree) is ast.BitXor:
        return '^'
    elif type(tree) is ast.BoolOp:
        return '(%s)' % code(tree.op).join([code(val) for val in tree.values])
    elif type(tree) is ast.Break:
        return '__break(__d)'
    elif type(tree) is ast.Call:
        func = code(tree.func)
        args = [code(arg) for arg in tree.args]
        keywords = [code(kw) for kw in tree.keywords]
        if tree.starargs is None:
            starargs = []
        else:
            starargs = ["*"+code(tree.starargs)]
        if tree.kwargs is None:
            kwargs = []
        else:
            kwargs = ["**"+code(tree.kwargs)]
        elems = args + keywords + starargs + kwargs
        comma_sep_elems = ','.join(elems)
        return '%s(%s)' % (func, comma_sep_elems)
    elif type(tree) is ast.ClassDef:
        raise NotImplementedError('Not yet implemented: classdef')
        ## Note to self: delattr and setattr are useful things
        ## also you're DEFINITELY going to want this:
        ## https://docs.python.org/2/library/functions.html#type
    elif type(tree) is ast.Compare:
        assert len(tree.ops) == len(tree.comparators)
        return code(tree.left) + ''.join([code(tree.ops[i])+code(tree.comparators[i]) for i in range(len(tree.ops))])
    elif type(tree) is ast.comprehension:
        return ('for %s in %s' % (code(tree.target), code(tree.iter))) + ''.join([' if '+code(i) for i in tree.ifs])
    elif type(tree) is ast.Continue:
        return '__continue(__d)'
    elif type(tree) is ast.Delete:
        return '(lambda *___: %s)(%s)' % (after, ', '.join(map(delete_code, tree.targets)))
    elif type(tree) is ast.Dict:
        return '{%s}' % ','.join([('%s:%s'%(code(k), code(v))) for (k,v) in zip(tree.keys, tree.values)])
    elif type(tree) is ast.DictComp:
        return '{%s}' % (' '.join([code(tree.key)+":"+code(tree.value)] + [code(gen) for gen in tree.generators]))
    elif type(tree) is ast.Div:
        return '/'
    elif type(tree) is ast.Ellipsis:
        return '...'
    elif type(tree) is ast.Eq:
        return '=='
    elif type(tree) is ast.ExceptHandler:
        raise NotImplementedError('Open problem: except')
    elif type(tree) is ast.Exec:
        exec_code = '__exec(%s, %s, %s)' % (
            code(tree.body),
            '__d.__dict__' if tree.globals is None else code(tree.globals),
            '__d.__dict__' if tree.locals is None else code(tree.locals))
        if after != 'None':
            return '(lambda ___: %s)(%s)' % (after, exec_code)
        else:
            return exec_code
    elif type(tree) is ast.Expr:
        code_to_exec = code(tree.value)
        return '(lambda ___: %s)(%s)' % (after, code_to_exec) ## TODO: ensure ___ isn't taken
    elif type(tree) is ast.Expression:
        return code(tree.body)
    elif type(tree) is ast.ExtSlice:
        return ' '.join(code(dim) + ',' for dim in tree.dims)
    elif type(tree) is ast.FloorDiv:
        return '//'
    elif type(tree) is ast.For:
        item = code(tree.target)
        body = many_to_one(tree.body, after='__this(__d)')
        items = code(tree.iter)
        orelse = many_to_one(tree.orelse, after='__after(__d)')
        return lambda_function({'__items': 'iter(%s)' % items, '__sentinel': '[]', '__after': 'lambda __d: %s' % after}) % \
            ('__y(lambda __this: lambda __d: %s)(__d)' %
             (lambda_function({'__i': 'next(__items, __sentinel)'}) %
              ('%s if __i is not __sentinel else %s' %
               (lambda_function({'__break': '__after', '__continue': '__this'}) %
                assignment_component(body, '%s' % item, '__i'),
                orelse))))
    elif type(tree) is ast.FunctionDef:
        args, arg_names = code(tree.args) ## of the form ('lambda x, y, z=5, *args:', ['x','y','z','args'])
        body = many_to_one(tree.body)
        body = assignment_component(body, ','.join('__d.' + name for name in arg_names) or '[]', ','.join(arg_names)) ## apply lets for d.arguments
        function_code = args + body
        for decorator in reversed(tree.decorator_list):
            function_code = "%s(%s)" % (code(decorator), function_code)
        return assignment_component(after, "__d."+tree.name, function_code)
    elif type(tree) is ast.arguments:
        ## return something of the form ('lambda x, y, z=5, *args:', ['x','y','z','args'])
        padded_defaults = [None]*(len(tree.args)-len(tree.defaults)) + tree.defaults
        arg_names = [arg.id for arg in tree.args]
        args = zip(padded_defaults, tree.args)
        args = [a.id if d is None else a.id+"="+code(d) for (d,a) in args]
        if tree.vararg is not None:
            args += ["*" + tree.vararg]
            arg_names += [tree.vararg]
        if tree.kwarg is not None:
            args += ["**" + tree.kwarg]
            arg_names += [tree.kwarg]
        args = ",".join(args)
        return ("lambda %s:" % (args), arg_names)
    elif type(tree) is ast.GeneratorExp:
        return '(%s)' % (' '.join([code(tree.elt)] + [code(gen) for gen in tree.generators]))
    elif type(tree) is ast.Global:
        raise NotImplementedError('Open problem: global')
    elif type(tree) is ast.Gt:
        return '>'
    elif type(tree) is ast.GtE:
        return '>='
    elif type(tree) is ast.If:
        test = code(tree.test)
        body = many_to_one(tree.body, after='__after(__d)')
        orelse = many_to_one(tree.orelse, after='__after(__d)')
        return "(lambda __after: %s if %s else %s)(lambda __d: %s)" % (body, test, orelse, after)
    elif type(tree) is ast.IfExp:
        return "(%s if %s else %s)" % (code(tree.body), code(tree.test), code(tree.orelse))
    elif type(tree) is ast.Import:
        for alias in tree.names:
            ids = alias.name.split('.')
            if alias.asname is None:
                after = assignment_component(after, "__d.%s"%ids[0], "__import__(%r, __d.__dict__, __d.__dict__)"%alias.name)
            else:
                after = assignment_component(after, "__d.%s"%alias.asname, '.'.join(["__import__(%r, __d.__dict__, __d.__dict__)"%alias.name] + ids[1:]))
        return after
    elif type(tree) is ast.ImportFrom:
        return '(lambda __mod: %s)(__import__(%r, __d.__dict__, __d.__dict__, %r, %r))' % (
            assignment_component(
                after,
                ','.join('__d.' + (alias.name if alias.asname is None else alias.asname) for alias in tree.names),
                ','.join('__mod.' + alias.name for alias in tree.names)),
            '' if tree.module is None else tree.module,
            tuple(alias.name for alias in tree.names),
            tree.level)
        raise NotImplementedError('Open problem: importfrom')
    elif type(tree) is ast.In:
        return ' in '
    elif type(tree) is ast.Index:
        return '%s' % code(tree.value)
    elif type(tree) is ast.Interactive:
        return INIT_CODE % many_to_one(child_nodes(tree))
    elif type(tree) is ast.Invert:
        return '~'
    elif type(tree) is ast.Is:
        return ' is '
    elif type(tree) is ast.IsNot:
        return ' is not '
    elif type(tree) is ast.LShift:
        return '<<'
    elif type(tree) is ast.keyword:
        return '%s=%s' % (tree.arg, code(tree.value))
    elif type(tree) is ast.Lambda:
        args, arg_names = code(tree.args)
        body = code(tree.body)
        body = assignment_component(body, ','.join('__d.' + name for name in arg_names) or '[]', ','.join(arg_names))
        return '(' + args + body + ')'
    elif type(tree) is ast.List:
        elts = [code(elt) for elt in tree.elts]
        return '[%s]' % (','.join(elts))
    elif type(tree) is ast.ListComp:
        return '[%s]' % (' '.join([code(tree.elt)] + [code(gen) for gen in tree.generators]))
    elif type(tree) is ast.Lt:
        return '<'
    elif type(tree) is ast.LtE:
        return '<='
    elif type(tree) is ast.Mod:
        return '%'
    elif type(tree) is ast.Module:
        ## Todo: look into sys.stdout instead
        return INIT_CODE % many_to_one(child_nodes(tree))
    elif type(tree) is ast.Mult:
        return '*'
    elif type(tree) is ast.Name:
        return '__d.'+tree.id
    elif type(tree) is ast.Not:
        return 'not '
    elif type(tree) is ast.NotEq:
        return '!='
    elif type(tree) is ast.NotIn:
        return ' not in '
    elif type(tree) is ast.Num:
        return repr(tree.n)
    elif type(tree) is ast.Or:
        return ' or '
    elif type(tree) is ast.Pass:
        return after
    elif type(tree) is ast.Pow:
        return '**'
    elif type(tree) is ast.Print:
        to_print = ','.join([code(x) for x in tree.values])
        if after != 'None':
            return '(lambda ___: %s)(__print(%s))' % (after, to_print) ## TODO: ensure ___ isn't taken
        else:
            return '__print(%s)' % to_print
    elif type(tree) is ast.RShift:
        return '>>'
    elif type(tree) is ast.Raise:
        if tree.type is None:
            return '([] for [] in []).throw(*sys.exc_info())'
        else:
            return '([] for [] in []).throw(%s%s%s)' % (
                code(tree.type),
                '' if tree.inst is None else ', ' + code(tree.inst),
                '' if tree.tback is None else ', ' + code(tree.tback))
    elif type(tree) is ast.Repr:
        return 'repr(%s)' % code(tree.value)
    elif type(tree) is ast.Return:
        return code(tree.value)
    elif type(tree) is ast.Set:
        assert tree.elts, '{} is a dict'
        return '{%s}' % ', '.join(code(elt) for elt in tree.elts)
    elif type(tree) is ast.SetComp:
        return '{%s}' % (' '.join([code(tree.elt)] + [code(gen) for gen in tree.generators]))
    elif type(tree) is ast.Slice:
        return '%s:%s%s' % (
            '' if tree.lower is None else code(tree.lower),
            '' if tree.upper is None else code(tree.upper),
            '' if tree.step is None else ':' + code(tree.step))
    elif type(tree) is ast.Str:
        return repr(tree.s)
    elif type(tree) is ast.Sub:
        return '-'
    elif type(tree) is ast.Subscript:
        return '%s[%s]' % (code(tree.value), code(tree.slice))
    elif type(tree) is ast.Suite:
        return INIT_CODE % many_to_one(child_nodes(tree))
    elif type(tree) is ast.TryExcept:
        raise NotImplementedError('Open problem: try-except')
    elif type(tree) is ast.TryFinally:
        raise NotImplementedError('Open problem: try-finally')
    elif type(tree) is ast.Tuple:
        elts = [code(elt) for elt in tree.elts]
        if len(elts) is 0:
            return '()'
        elif len(elts) is 1:
            return '(%s,)' % elts[0]
        else:
            return '(%s)' % (','.join(elts))
    elif type(tree) is ast.UAdd:
        return '+'
    elif type(tree) is ast.USub:
        return '-'
    elif type(tree) is ast.UnaryOp:
        return '(%s%s)' % (code(tree.op), code(tree.operand))
    elif type(tree) is ast.While:
        test = code(tree.test)
        body = many_to_one(tree.body, after='__this(__d)')
        orelse = many_to_one(tree.orelse, after='__after(__d)')
        return lambda_function({'__after': 'lambda __d: %s' % after}) % \
            ('__y(lambda __this: lambda __d: %s if %s else %s)(__d)' %
             (lambda_function({'__break': '__after', '__continue': '__this'}) % body,
              test, orelse))
    elif type(tree) is ast.With:
        raise NotImplementedError('Open problem: with')
    elif type(tree) is ast.Yield:
        raise NotImplementedError('Open problem: yield')
    else:
        raise NotImplementedError('Case not caught: %s' % str(type(tree)))




## The entry point for everything.
def to_one_line(original):
    ## original :: string
    ## :: string
    global INIT_CODE

    t = ast.parse(original)

    original = original.strip()

    ## If there's only one line anyways, be lazy
    if len(original.splitlines()) == 1 and \
       type(t) is ast.Module and \
       len(t.body) == 1 and \
       type(t.body[0]) in (ast.Delete, ast.Assign, ast.AugAssign, ast.Print, ast.Raise, ast.Assert, ast.Import, ast.ImportFrom, ast.Exec, ast.Global, ast.Expr, ast.Pass):
        return original

    INIT_CODE = get_init_code(t)

    return code(t)


# def has_single_print(tree):
#     ## TODO analysis for this
#     ## Return (True, ASTExpressionNode) if there is a single print (where ASTNode is the thing to be printeeee---
#     ## wait what if it's in a function k nevermind
#     return (False, None)





DEBUG = True ## TODO: Use command line arg instead



if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "Usage: python main.py inputfilename [outputfilename]"
    else:
        infilename = sys.argv[1]

        if len(sys.argv) >= 3:
            outfilename = sys.argv[2]
        else:
            if ".py" in infilename:
                outfilename = ".ol.py".join(infilename.rsplit(".py", 1))
            else:
                outfilename = infilename + ".ol.py"
            print "Writing to %s" % outfilename

        infi = open(infilename, 'r')
        outfi = open(outfilename, 'w')

        original = infi.read().strip()
        onelined = to_one_line(original)
        outfi.write(onelined+"\n")

        if DEBUG:
            print '--- ORIGINAL ---------------------------------'
            print original
            print '----------------------------------------------'
            try:
                exec(original)
            except Exception as e:
                print e
            print '--- ONELINED ---------------------------------'
            print onelined
            print '----------------------------------------------'
            try:
                exec(onelined)
            except Exception as e:
                print e
