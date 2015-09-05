import argparse
import ast
import sys
from template import T


# TODO: Detect which features are ACTUALLY needed, and modify the code
# accordingly.

# Need __d and the list comprehension trick if we do anything involving __d --
# while, for, if
# Need __print if we print
# Need __y if we use while
# Need __builtin__ if we use __print OR if we use __d

# Abstractions for naming of variables.
DUNDER_PRINT = "__print"
DUNDER_EXEC = "__exec"
DUNDER_Y = "__y"
DUNDER_D = "__d"


def lambda_function(arguments_to_values, prettyprinted=False):
    # arguments_to_values :: {argument_i: value_i}
    # :: string
    if prettyprinted:
        raise NotImplementedError
    else:
        return T('(lambda {}: {})({})').format(
            T(', ').join(arguments_to_values.keys()),
            T('{}'),
            T(', ').join(arguments_to_values.values()))


def get_init_code(tree):
    # Calculate the helper variables that we will need, and return a string
    # which defines those variables and leaves a {} where the rest of the code
    # will need to continue.

    # TODO: Short-circuit to something far simpler if the program has but one
    # print statement.

    # TODO: Calculate these booleans.
    need_print = True  # true if prints anywhere.
    need_exec = True  # true if execs anywhere.
    need_y_combinator = True  # true if uses a while.
    need_state_dict = True  # true if uses anything involving __d - while, for,
                            # if. Also governs the list comprehension trick.
    need_dunderbuiltin = need_print or need_state_dict
    need_sys = True  # true if anything uses raise with no arguments, del a[:],
                     # or del a[n:].

    output = T('{}')
    if need_dunderbuiltin:
        output = output.format(lambda_function({"__builtin__":
                                                "__import__('__builtin__')"}))

    arguments = {}
    if need_print:
        arguments[DUNDER_PRINT] = "__builtin__.__dict__['print']"
    if need_exec:
        arguments[DUNDER_EXEC] = ("__import__('trace').Trace(count=False,"
                                  " trace=False).runctx")
    if need_y_combinator:
        arguments[DUNDER_Y] = ("(lambda f: (lambda x: x(x))(lambda y:"
                               " f(lambda: y(y)())))")
    if need_state_dict:
        arguments[DUNDER_D] = "type('StateDict',(),__builtin__.__dict__)()"
    if need_sys:
        arguments['sys'] = "__import__('sys')"

    if len(arguments.keys()) > 0:
        output = output.format(lambda_function(arguments))

    return output


boolop_code = {
    ast.And: ' and ',
    ast.Or: ' or ',
}

operator_code = {
    ast.Add: '+',
    ast.Sub: '-',
    ast.Mult: '*',
    ast.Div: '/',
    ast.Mod: '%',
    ast.Pow: '**',
    ast.LShift: '<<',
    ast.RShift: '>>',
    ast.BitOr: '|',
    ast.BitXor: '^',
    ast.BitAnd: '&',
    ast.FloorDiv: '//',
}

unaryop_code = {
    ast.Invert: '~',
    ast.Not: 'not ',
    ast.UAdd: '+',
    ast.USub: '-',
}

cmpop_code = {
    ast.Eq: '==',
    ast.NotEq: '!=',
    ast.Lt: '<',
    ast.LtE: '<=',
    ast.Gt: '>',
    ast.GtE: '>=',
    ast.Is: ' is ',
    ast.IsNot: ' is not ',
    ast.In: ' in ',
    ast.NotIn: ' not in ',
}

def many_to_one(trees, after='None'):
    # trees :: [Tree]
    # return :: string
    assert type(trees) is list
    if len(trees) is 0:
        return T('{}').format(after)
    else:
        return code_with_after(trees[0], many_to_one(trees[1:], after=after))


def code(tree):
    return code_with_after(tree, 'None')


def assignment_component(after, targets, value):
    # return T('(lambda {}: {})({})').format(targets, after, value)
    return T('[{} for {} in [({})]][0]').format(after, targets, value)


def slice_repr(slice):
    if type(slice) is ast.Ellipsis:
        return T('Ellipsis')
    elif type(slice) is ast.Slice:
        return T('slice({}, {}, {})').format(
            'None' if slice.lower is None else code(slice.lower),
            'None' if slice.upper is None else code(slice.upper),
            'None' if slice.step is None else code(slice.step))
    elif type(slice) is ast.ExtSlice:
        return T('({})').format(T(' ').join(slice_repr(dim) + ',' for dim in slice.dims))
    elif type(slice) is ast.Index:
        return code(slice.value)
    else:
        raise NotImplementedError('Case not caught: %s' % str(type(slice)))


def delete_code(target):
    if type(target) is ast.Attribute:
        return [T('delattr({}, {!r})').format(code(target.value), target.attr)]
    elif type(target) is ast.Subscript:
        if type(target.slice) is ast.Slice and target.slice.step is None:
            return [lambda_function({'__value': code(target.value)}).format(
                T("getattr(__value, '__delslice__', lambda __lower, __upper: "
                  "__value.__delitem__(slice({}, {})))({}, {})").format(
                      'None' if target.slice.lower is None else '__lower',
                      'None' if target.slice.upper is None else '__upper',
                      '0' if target.slice.lower is None
                          else code(target.slice.lower),
                      'sys.maxint' if target.slice.upper is None
                          else code(target.slice.upper)))]
        else:
            return [T('{}.__delitem__({})').format(code(target.value),
                                                   slice_repr(target.slice))]
    elif type(target) is ast.Name:
        return [T('delattr(__d, {!r})').format(target.id)]
    elif type(target) in (ast.List, ast.Tuple):
        return [c for elt in target.elts for c in delete_code(elt)]
    else:
        raise NotImplementedError('Case not caught: %s' % str(type(target)))


def code_with_after(tree, after):
    if type(tree) is ast.Assert:
        return T('({} if {} else ([] for [] in []).throw(AssertionError{}))').format(
            after, code(tree.test),
            '' if tree.msg is None else T('({})').format(code(tree.msg)))
    elif type(tree) is ast.Assign:
        targets = [code(target) for target in tree.targets]
        value = code(tree.value)
        targets = T(',').join(targets)
        return assignment_component(after, targets,
            value if len(tree.targets) == 1
                  else T('[{}]*{}').format(value, len(tree.targets)))
    elif type(tree) is ast.Attribute:
        return T('{}.{}').format(code(tree.value), tree.attr)
    elif type(tree) is ast.AugAssign:
        target = code(tree.target)
        op = operator_code[type(tree.op)]
        iop = type(tree.op).__name__.lower()
        if iop.startswith('bit'):
            iop = iop[len('bit'):]
        iop = '__i%s__' % iop
        value = code(tree.value)
        value = T('(lambda __target, __value: (lambda __ret: __target {} '
                  '__value if __ret is NotImplemented else __ret)(getattr('
                  '__target, {!r}, lambda other: NotImplemented)(__value)))({}, '
                  '{})').format(op, iop, target, value)
        return assignment_component(after, target, value)
    elif type(tree) is ast.BinOp:
        return T('({}{}{})').format(code(tree.left), operator_code[type(tree.op)], code(tree.right))
    elif type(tree) is ast.BoolOp:
        return T('({})').format(T(boolop_code[type(tree.op)]).join(map(code, tree.values)))
    elif type(tree) is ast.Break:
        return T('__break()')
    elif type(tree) is ast.Call:
        func = code(tree.func)
        args = [code(arg) for arg in tree.args]
        keywords = [code(kw) for kw in tree.keywords]
        if tree.starargs is None:
            starargs = []
        else:
            starargs = ["*" + code(tree.starargs)]
        if tree.kwargs is None:
            kwargs = []
        else:
            kwargs = ["**" + code(tree.kwargs)]
        elems = args + keywords + starargs + kwargs
        comma_sep_elems = T(',').join(elems)
        return T('{}({})').format(func, comma_sep_elems)
    elif type(tree) is ast.ClassDef:
        raise NotImplementedError('Not yet implemented: classdef')
        # Note to self: delattr and setattr are useful things
        # also you're DEFINITELY going to want this:
        # https://docs.python.org/2/library/functions.html#type
    elif type(tree) is ast.Compare:
        assert len(tree.ops) == len(tree.comparators)
        return code(tree.left) + T('').join(
            [cmpop_code[type(tree.ops[i])] + code(tree.comparators[i])
             for i in range(len(tree.ops))])
    elif type(tree) is ast.comprehension:
        return (T('for {} in {}').format(code(tree.target), code(tree.iter)) +
                T('').join(' if ' + code(i) for i in tree.ifs))
    elif type(tree) is ast.Continue:
        return T('__continue()')
    elif type(tree) is ast.Delete:
        cs = [c for target in tree.targets for c in delete_code(target)]
        if cs:
            return T('({}, {})[-1]').format(T(', ').join(cs), after)
        else:
            return T('{}').format(after)
    elif type(tree) is ast.Dict:
        return T('{{{}}}').format(T(',').join((T('{}:{}').format(code(k), code(v)))
                                              for (k, v) in zip(tree.keys, tree.values)))
    elif type(tree) is ast.DictComp:
        return T('{{{}}}').format(T(' ').join([code(tree.key) + ":" + code(tree.value)] +
                                              map(code, tree.generators)))
    elif type(tree) is ast.Ellipsis:
        return T('...')
    elif type(tree) is ast.ExceptHandler:
        raise NotImplementedError('Open problem: except')
    elif type(tree) is ast.Exec:
        exec_code = T('__exec({}, {}, {})').format(
            code(tree.body),
            '__d.__dict__' if tree.globals is None else code(tree.globals),
            '__d.__dict__' if tree.locals is None else code(tree.locals))
        if after != 'None':
            return T('({}, {})[1]').format(exec_code, after)
        else:
            return exec_code
    elif type(tree) is ast.Expr:
        return T('({}, {})[1]').format(code(tree.value), after)
    elif type(tree) is ast.Expression:
        return code(tree.body)
    elif type(tree) is ast.ExtSlice:
        return T(' ').join(code(dim) + ',' for dim in tree.dims)
    elif type(tree) is ast.For:
        item = code(tree.target)
        body = many_to_one(tree.body, after='__this()')
        items = code(tree.iter)
        orelse = many_to_one(tree.orelse, after='__after()')
        return lambda_function({'__items': T('iter({})').format(items), '__sentinel':
                                '[]', '__after': T('lambda: {}').format(after)}).format(
            T('__y(lambda __this: lambda: {})()').format(
                lambda_function({'__i': 'next(__items, __sentinel)'}).format(
                    T('{} if __i is not __sentinel else {}').format(
                        lambda_function({'__break': '__after',
                                         '__continue': '__this'}).format(
                            assignment_component(body, item, '__i')),
                        orelse))))
    elif type(tree) is ast.FunctionDef:
        # code() returns something of the form
        # ('lambda x, y, z=5, *args:', ['x','y','z','args'])
        args, arg_names = code(tree.args)
        body = many_to_one(tree.body)
        if arg_names:
            body = assignment_component(body,
                T(',').join('__d.' + name for name in arg_names),
                T(',').join(arg_names))
        function_code = args + body
        for decorator in reversed(tree.decorator_list):
            function_code = T('{}({})').format(code(decorator), function_code)
        return assignment_component(
            after,
            T('{}, {}.__name__').format('__d.' + tree.name, '__d.' + tree.name),
            T('{}, {!r}').format(function_code, tree.name))
    elif type(tree) is ast.arguments:
        # this should return something of the form
        # ('lambda x, y, z=5, *args:', ['x','y','z','args'])
        padded_defaults = [None] * (len(tree.args) -
                                    len(tree.defaults)) + tree.defaults
        arg_names = [arg.id for arg in tree.args]
        args = zip(padded_defaults, tree.args)
        args = [a.id if d is None else a.id + "=" + code(d) for (d, a) in args]
        if tree.vararg is not None:
            args += ["*" + tree.vararg]
            arg_names += [tree.vararg]
        if tree.kwarg is not None:
            args += ["**" + tree.kwarg]
            arg_names += [tree.kwarg]
        args = T(',').join(args)
        return (T('lambda {}:').format(args), arg_names)
    elif type(tree) is ast.GeneratorExp:
        return T('({})').format(T(' ').join([code(tree.elt)] +
                                            map(code, tree.generators)))
    elif type(tree) is ast.Global:
        raise NotImplementedError('Open problem: global')
    elif type(tree) is ast.If:
        test = code(tree.test)
        body = many_to_one(tree.body, after='__after()')
        orelse = many_to_one(tree.orelse, after='__after()')
        return T('(lambda __after: {} if {} else {})(lambda: {})').format(
            body, test, orelse, after)
    elif type(tree) is ast.IfExp:
        return T('({} if {} else {})').format(
            code(tree.body), code(tree.test), code(tree.orelse))
    elif type(tree) is ast.Import:
        after = T('{}').format(after)
        for alias in tree.names:
            ids = alias.name.split('.')
            if alias.asname is None:
                after = assignment_component(after, T('__d.{}').format(ids[0]),
                    T('__import__({!r}, __d.__dict__, __d.__dict__)').format(alias.name))
            else:
                after = assignment_component(after, T('__d.{}').format(alias.asname),
                    T('.').join([T('__import__({!r}, __d.__dict__, __d.__dict__)').format(
                        alias.name)] + ids[1:]))
        return after
    elif type(tree) is ast.ImportFrom:
        return T('(lambda __mod: {})(__import__({!r}, __d.__dict__, __d.__dict__,'
                 ' {!r}, {!r}))').format(
            assignment_component(
                after,
                T(',').join('__d.' + (alias.name if alias.asname is None
                                      else alias.asname) for alias in tree.names),
                T(',').join('__mod.' + alias.name for alias in tree.names)),
            '' if tree.module is None else tree.module,
            tuple(alias.name for alias in tree.names),
            tree.level)
    elif type(tree) is ast.Index:
        return code(tree.value)
    elif type(tree) is ast.keyword:
        return T('{}={}').format(tree.arg, code(tree.value))
    elif type(tree) is ast.Lambda:
        args, arg_names = code(tree.args)
        body = code(tree.body)
        if arg_names:
            body = assignment_component(body, T(',').join('__d.' + name
                for name in arg_names), T(',').join(arg_names))
        return '(' + args + body + ')'
    elif type(tree) is ast.List:
        elts = [code(elt) for elt in tree.elts]
        return T('[{}]').format(T(',').join(elts))
    elif type(tree) is ast.ListComp:
        return T('[{}]').format(T(' ').join([code(tree.elt)] +
                                            map(code, tree.generators)))
    elif type(tree) is ast.Name:
        return T('__d.') + tree.id
    elif type(tree) is ast.Num:
        return T('{!r}').format(tree.n)
    elif type(tree) is ast.Pass:
        return T('{}').format(after)
    elif type(tree) is ast.Print:
        to_print = T(',').join(code(x) for x in tree.values)
        if tree.dest is not None:
            # Abuse varargs to get the right evaluation order
            to_print = T('file={}, *[{}]').format(code(tree.dest), to_print)
        if not tree.nl:
            # TODO: This is apparently good enough for 2to3, but gets
            # many cases wrong (tests/unimplemented/softspace.py).
            to_print += ", end=' '"
        if after != 'None':
            return T('(__print({}), {})[1]').format(to_print, after)
        else:
            return T('__print({})').format(to_print)
    elif type(tree) is ast.Raise:
        if tree.type is None:
            return T('([] for [] in []).throw(*sys.exc_info())')
        else:
            return T('([] for [] in []).throw({}{}{})').format(
                code(tree.type),
                '' if tree.inst is None else ', ' + code(tree.inst),
                '' if tree.tback is None else ', ' + code(tree.tback))
    elif type(tree) is ast.Repr:
        return T('`{}`').format(code(tree.value))
    elif type(tree) is ast.Return:
        return code(tree.value)
    elif type(tree) is ast.Set:
        assert tree.elts, '{} is a dict'
        return T('{{{}}}').format(T(', ').join(code(elt) for elt in tree.elts))
    elif type(tree) is ast.SetComp:
        return T('{{{}}}').format(T(' ').join([code(tree.elt)] +
                                              map(code, tree.generators)))
    elif type(tree) is ast.Slice:
        return T('{}:{}{}').format(
            '' if tree.lower is None else code(tree.lower),
            '' if tree.upper is None else code(tree.upper),
            '' if tree.step is None else ':' + code(tree.step))
    elif type(tree) is ast.Str:
        return T('{!r}').format(tree.s)
    elif type(tree) is ast.Subscript:
        return T('{}[{}]').format(code(tree.value), code(tree.slice))
    elif type(tree) is ast.TryExcept:
        raise NotImplementedError('Open problem: try-except')
    elif type(tree) is ast.TryFinally:
        raise NotImplementedError('Open problem: try-finally')
    elif type(tree) is ast.Tuple:
        elts = [code(elt) for elt in tree.elts]
        if len(elts) is 0:
            return T('()')
        elif len(elts) is 1:
            return T('({},)').format(elts[0])
        else:
            return T('({})').format(T(',').join(elts))
    elif type(tree) is ast.UnaryOp:
        return T('({}{})').format(unaryop_code[type(tree.op)], code(tree.operand))
    elif type(tree) is ast.While:
        test = code(tree.test)
        body = many_to_one(tree.body, after='__this()')
        orelse = many_to_one(tree.orelse, after='__after()')
        return lambda_function({'__after': T('lambda: {}').format(after)}).format(
            T('__y(lambda __this: lambda: {} if {} else {})()').format(
                lambda_function({'__break': '__after', '__continue': '__this'}).format(
                    body), test, orelse))
    elif type(tree) is ast.With:
        raise NotImplementedError('Open problem: with')
    elif type(tree) is ast.Yield:
        raise NotImplementedError('Open problem: yield')
    else:
        raise NotImplementedError('Case not caught: %s' % str(type(tree)))


# The entry point for everything.
def to_one_line(original):
    # original :: string
    # :: string
    t = ast.parse(original)

    original = original.strip()

    # If there's only one line anyways, be lazy
    if len(original.splitlines()) == 1 and \
       len(t.body) == 1 and \
       type(t.body[0]) in (ast.Delete, ast.Assign, ast.AugAssign, ast.Print,
                           ast.Raise, ast.Assert, ast.Import, ast.ImportFrom,
                           ast.Exec, ast.Global, ast.Expr, ast.Pass):
        return original

    return get_init_code(t).format(many_to_one(t.body)).close()


# TODO: Use command line arg instead
DEBUG = True


if __name__ == '__main__':
    usage = ['python main.py --help',
            'python main.py infile.py outfile.py',
            'cat infile > python main.py outfile.py',
            'cat infile > python main.py > outfile.py'
            ]
    parser = argparse.ArgumentParser(usage='\n       '.join(usage),
        description=("if infile is given and outfile is not, outfile will be "
                     "infile.ol.py"))
    parser.add_argument('file_one', nargs='?')
    parser.add_argument('file_two', nargs='?')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    original = None
    if args.file_one is None:
        # I have gotten no arguments. Look at sys.stdin
        if sys.stdin.isatty():
            sys.exit('No input. see python main.py --help')
        original = sys.stdin.read()
        outfilename = None
    elif args.file_two is None:
        # I have gotten one argument. If there's something to read from
        # sys.stdin, read from there.
        if sys.stdin.isatty():  # nothing at sys.stdin
            if 'py' in args.file_one:
                outfilename = '.ol.py'.join(args.file_one.rsplit(".py", 1))
            else:
                outfilename = args.file_one + '.ol.py'
        else:  # I see something at sys.stdin
            original = sys.stdin.read()
            outfilename = args.file_one
    else:
        if not sys.stdin.isatty():
            sys.exit('why did you give me something on sys.stdin?')
        outfilename = args.file_two

    if original is None:
        infile = open(args.file_one)
        original = infile.read().strip()
        infile.close()
    onelined = to_one_line(original)
    if outfilename is None:
        print onelined
    else:
        outfi = open(outfilename, 'w')
        outfi.write(onelined + '\n')
        outfi.close()

    if args.debug:
        if outfilename is None:
            # redirect to sys.stderr if I'm writing outfile to sys.stdout
            sys.stdout = sys.stderr
        print '--- ORIGINAL ---------------------------------'
        print original
        print '----------------------------------------------'
        scope = {}
        try:
            exec(original, scope)
        except Exception as e:
            print e
        print '--- ONELINED ---------------------------------'
        print onelined
        print '----------------------------------------------'
        scope = {}
        try:
            exec(onelined, scope)
        except Exception as e:
            print e
