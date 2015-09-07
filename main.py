import argparse
import ast
import symtable
import sys
from template import T


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

def provide(body, **subs):
    body = T('{}').format(body)
    needed = set(body.free()).intersection(subs)
    if needed:
        return lambda_function({k: subs[k] for k in needed}).format(
            body.format(**{k: k for k in needed}))
    else:
        return body


def get_init_code(output):
    # Calculate the helper variables that we will need, wrap the output
    # code in a definition of those variables.

    # TODO: Short-circuit to something far simpler if the program has but one
    # print statement.

    output = provide(
        output.format(__l=T('{__g}')),
        __print=T("{__builtin__}.__dict__['print']"),
        __exec="__import__('trace').Trace(count=False,"
               " trace=False).runctx",
        __y="(lambda f: (lambda x: x(x))(lambda y:"
          " f(lambda: y(y)())))",
        __g=T("{__builtin__}.__dict__.copy()"),
        sys="__import__('sys')")

    output = provide(
        output,
        __builtin__="__import__('__builtin__')")

    return output.close()


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


def assignment_component(after, targets, value):
    # return T('(lambda {}: {})({})').format(targets, after, value)
    return T('[{} for {} in [({})]][0]').format(after, targets, value)


class Namespace(ast.NodeVisitor):
    def __init__(self, table):
        self.table = table
        self.subtables = iter(table.get_children())

    def var(self, name):
        sym = self.table.lookup(name)
        if sym.is_global():
            return T('{__g}[{!r}]').format(name)
        elif sym.is_local():
            return T('{__l}[{!r}]').format(name)
        elif sym.is_free():
            return T('{__f}[{!r}]()').format(name)
        else:
            raise SyntaxError('confusing symbol {!r}'.format(name))

    def delete_var(self, name):
        sym = self.table.lookup(name)
        if sym.is_global():
            return T('{__g}.pop({!r})').format(name)
        elif sym.is_local():
            return T('{__l}.pop({!r})').format(name)
        elif sym.is_free():
            raise SyntaxError('deleting free variable {!r}'.format(name))
        else:
            raise SyntaxError('confusing symbol {!r}'.format(name))

    def close(self, ns, body, **subs):
        return provide(
            body,
            __l='{}',
            __f=T('{{{}}}').format(T(', ').join(
                T('{!r}: lambda: {}').format(v, self.var(v)) for v in ns.table.get_frees())),
            **subs)

    def many_to_one(self, trees, after='None'):
        # trees :: [Tree]
        # return :: string
        return reduce(
            lambda ctx, tree: ctx.format(after=self.visit(tree)),
            trees,
            T('{after}')).format(after=after)

    def slice_repr(self, slice):
        if type(slice) is ast.Ellipsis:
            return T('Ellipsis')
        elif type(slice) is ast.Slice:
            return T('slice({}, {}, {})').format(
                'None' if slice.lower is None else self.visit(slice.lower),
                'None' if slice.upper is None else self.visit(slice.upper),
                'None' if slice.step is None else self.visit(slice.step))
        elif type(slice) is ast.ExtSlice:
            return T('({})').format(T(' ').join(self.slice_repr(dim) + ',' for dim in slice.dims))
        elif type(slice) is ast.Index:
            return self.visit(slice.value)
        else:
            raise NotImplementedError('Case not caught: %s' % str(type(slice)))

    def delete_code(self, target):
        if type(target) is ast.Attribute:
            return [T('delattr({}, {!r})').format(self.visit(target.value), target.attr)]
        elif type(target) is ast.Subscript:
            if type(target.slice) is ast.Slice and target.slice.step is None:
                return [lambda_function({'__value': self.visit(target.value)}).format(
                    T("getattr(__value, '__delslice__', lambda __lower, __upper: "
                      "__value.__delitem__(slice({}, {})))({}, {})").format(
                          'None' if target.slice.lower is None else '__lower',
                          'None' if target.slice.upper is None else '__upper',
                          '0' if target.slice.lower is None
                              else self.visit(target.slice.lower),
                          T('{sys}.maxint') if target.slice.upper is None
                              else self.visit(target.slice.upper)))]
            else:
                return [T('{}.__delitem__({})').format(self.visit(target.value),
                                                       self.slice_repr(target.slice))]
        elif type(target) is ast.Name:
            return [self.delete_var(target.id)]
        elif type(target) in (ast.List, ast.Tuple):
            return [c for elt in target.elts for c in self.delete_code(elt)]
        else:
            raise NotImplementedError('Case not caught: %s' % str(type(target)))

    def visit_Assert(self, tree):
        return T('({after} if {} else ([] for [] in []).throw(AssertionError{}))').format(
            self.visit(tree.test),
            '' if tree.msg is None else T('({})').format(self.visit(tree.msg)))

    def visit_Assign(self, tree):
        targets = [self.visit(target) for target in tree.targets]
        value = self.visit(tree.value)
        targets = T(',').join(targets)
        return assignment_component(T('{after}'), targets,
            value if len(tree.targets) == 1
                  else T('[{}]*{}').format(value, len(tree.targets)))

    def visit_Attribute(self, tree):
        return T('{}.{}').format(self.visit(tree.value), tree.attr)

    def visit_AugAssign(self, tree):
        target = self.visit(tree.target)
        op = operator_code[type(tree.op)]
        iop = type(tree.op).__name__.lower()
        if iop.startswith('bit'):
            iop = iop[len('bit'):]
        iop = '__i%s__' % iop
        value = self.visit(tree.value)
        value = T('(lambda __target, __value: (lambda __ret: __target {} '
                  '__value if __ret is NotImplemented else __ret)(getattr('
                  '__target, {!r}, lambda other: NotImplemented)(__value)))({}, '
                  '{})').format(op, iop, target, value)
        return assignment_component(T('{after}'), target, value)

    def visit_BinOp(self, tree):
        return T('({}{}{})').format(self.visit(tree.left), operator_code[type(tree.op)], self.visit(tree.right))

    def visit_BoolOp(self, tree):
        return T('({})').format(T(boolop_code[type(tree.op)]).join(map(self.visit, tree.values)))

    def visit_Break(self, tree):
        return T('{__break}()')

    def visit_Call(self, tree):
        func = self.visit(tree.func)
        args = [self.visit(arg) for arg in tree.args]
        keywords = [self.visit(kw) for kw in tree.keywords]
        if tree.starargs is None:
            starargs = []
        else:
            starargs = ["*" + self.visit(tree.starargs)]
        if tree.kwargs is None:
            kwargs = []
        else:
            kwargs = ["**" + self.visit(tree.kwargs)]
        elems = args + keywords + starargs + kwargs
        comma_sep_elems = T(',').join(elems)
        return T('{}({})').format(func, comma_sep_elems)

    def visit_ClassDef(self, tree):
        raise NotImplementedError('Not yet implemented: classdef')
        # Note to self: delattr and setattr are useful things
        # also you're DEFINITELY going to want this:
        # https://docs.python.org/2/library/functions.html#type

    def visit_Compare(self, tree):
        assert len(tree.ops) == len(tree.comparators)
        return self.visit(tree.left) + T('').join(
            [cmpop_code[type(tree.ops[i])] + self.visit(tree.comparators[i])
             for i in range(len(tree.ops))])

    def visit_comprehension(self, tree):
        return (T('for {} in {}').format(self.visit(tree.target), self.visit(tree.iter)) +
                T('').join(' if ' + self.visit(i) for i in tree.ifs))

    def comprehension_code(self, generators, wrap):
        iter0 = self.visit(generators[0].iter)
        ns = Namespace(next(self.subtables))
        return self.close(
            ns,
            wrap(ns, T(' ').join(
                [T('for {} in {__iter}').format(ns.visit(generators[0].target))] +
                ['if ' + ns.visit(i) for i in generators[0].ifs] +
                map(ns.visit, generators[1:]))),
            __iter=iter0)

    def visit_Continue(self, tree):
        return T('{__continue}()')

    def visit_Delete(self, tree):
        cs = [c for target in tree.targets for c in self.delete_code(target)]
        if cs:
            return T('({}, {after})[-1]').format(T(', ').join(cs))
        else:
            return T('{after}')

    def visit_Dict(self, tree):
        return T('{{{}}}').format(T(',').join(
            T('{}:{}').format(k, v)
            for k, v in zip(map(self.visit, tree.keys), map(self.visit, tree.values))))

    def visit_DictComp(self, tree):
        return self.comprehension_code(
            tree.generators,
            lambda ns, g: T('{{{}: {} {}}}').format(
                T('{}'), ns.visit(tree.value), g).format(ns.visit(tree.key)))

    def visit_Ellipsis(self, tree):
        return T('...')

    def visit_ExceptHandler(self, tree):
        raise NotImplementedError('Open problem: except')

    def visit_Exec(self, tree):
        body = self.visit(tree.body)
        if tree.globals is None:
            exec_code = T('{__exec}({}, {__g}, {__l})').format(body)
        elif tree.locals is None:
            exec_code = T(
                '(lambda b, g: {__exec}(b, {__g} if g is None else g, '
                '{__l} if g is None else g))({}, {})').format(
                    body, self.visit(tree.globals))
        else:
            exec_code = T(
                '(lambda b, g, l: {__exec}(b, {__g} if g is None else g, '
                '({__l} if g is None else g) if l is None else l))({}, {}, {})').format(
                    body, self.visit(tree.globals), self.visit(tree.locals))
        return T('({}, {after})[1]').format(exec_code)

    def visit_Expr(self, tree):
        return T('({}, {after})[1]').format(self.visit(tree.value))

    def visit_Expression(self, tree):
        return self.visit(tree.body)

    def visit_ExtSlice(self, tree):
        return T(' ').join(self.visit(dim) + ',' for dim in tree.dims)

    def visit_For(self, tree):
        item = self.visit(tree.target)
        items = self.visit(tree.iter)
        body = self.many_to_one(tree.body, after='__this()')
        orelse = self.many_to_one(tree.orelse, after='__after()')
        return lambda_function({'__items': T('iter({})').format(items), '__sentinel':
                                '[]', '__after': T('lambda: {after}')}).format(
            T('{__y}(lambda __this: lambda: {})()').format(
                lambda_function({'__i': 'next(__items, __sentinel)'}).format(
                    T('{} if __i is not __sentinel else {}').format(
                        provide(
                            assignment_component(body, item, '__i'),
                            __break='__after', __continue='__this'),
                        orelse))))

    def visit_FunctionDef(self, tree):
        # self.visit() returns something of the form
        # ('lambda x, y, z=5, *args:', ['x','y','z','args'])
        args, arg_names = self.visit(tree.args)
        decoration = T('{}')
        for decorator in tree.decorator_list:
            decoration = decoration.format(T('{}({})').format(self.visit(decorator), T('{}')))
        ns = Namespace(next(self.subtables))
        body = ns.many_to_one(tree.body)
        if arg_names:
            body = assignment_component(body,
                T(',').join(ns.var(name) for name in arg_names),
                T(',').join(arg_names))
        body = self.close(ns, body)
        function_code = decoration.format(args + body)
        return assignment_component(
            T('{after}'),
            T('{}, {}.__name__').format(self.var(tree.name), self.var(tree.name)),
            T('{}, {!r}').format(function_code, tree.name))

    def visit_arguments(self, tree):
        # this should return something of the form
        # ('lambda x, y, z=5, *args:', ['x','y','z','args'])
        padded_defaults = [None] * (len(tree.args) -
                                    len(tree.defaults)) + tree.defaults
        arg_names = [arg.id for arg in tree.args]
        args = zip(padded_defaults, tree.args)
        args = [a.id if d is None else a.id + "=" + self.visit(d) for (d, a) in args]
        if tree.vararg is not None:
            args += ["*" + tree.vararg]
            arg_names += [tree.vararg]
        if tree.kwarg is not None:
            args += ["**" + tree.kwarg]
            arg_names += [tree.kwarg]
        args = T(',').join(args)
        return (T('lambda {}:').format(args), arg_names)

    def visit_GeneratorExp(self, tree):
        return self.comprehension_code(
            tree.generators,
            lambda ns, g: T('({} {})').format(ns.visit(tree.elt), g))

    def visit_Global(self, tree):
        raise NotImplementedError('Open problem: global')

    def visit_If(self, tree):
        test = self.visit(tree.test)
        body = self.many_to_one(tree.body, after='__after()')
        orelse = self.many_to_one(tree.orelse, after='__after()')
        return T('(lambda __after: {} if {} else {})(lambda: {after})').format(
            body, test, orelse)

    def visit_IfExp(self, tree):
        test = self.visit(tree.test)
        body = self.visit(tree.body)
        orelse = self.visit(tree.orelse)
        return T('({} if {} else {})').format(body, test, orelse)

    def visit_Import(self, tree):
        after = T('{after}')
        for alias in tree.names:
            ids = alias.name.split('.')
            if alias.asname is None:
                after = assignment_component(after, self.var(ids[0]),
                    T('__import__({!r}, {__g}, {__l})').format(alias.name))
            else:
                after = assignment_component(after, self.var(alias.asname),
                    T('.').join([T('__import__({!r}, {__g}, {__l})').format(
                        alias.name)] + ids[1:]))
        return after

    def visit_ImportFrom(self, tree):
        return T('(lambda __mod: {})(__import__({!r}, {__g}, {__l},'
                 ' {!r}, {!r}))').format(
            assignment_component(
                T('{after}'),
                T(',').join(self.var(alias.name if alias.asname is None
                                     else alias.asname) for alias in tree.names),
                T(',').join('__mod.' + alias.name for alias in tree.names)),
            '' if tree.module is None else tree.module,
            tuple(alias.name for alias in tree.names),
            tree.level)

    def visit_Index(self, tree):
        return self.visit(tree.value)

    def visit_keyword(self, tree):
        return T('{}={}').format(tree.arg, self.visit(tree.value))

    def visit_Lambda(self, tree):
        args, arg_names = self.visit(tree.args)
        ns = Namespace(next(self.subtables))
        body = ns.visit(tree.body)
        if arg_names:
            body = assignment_component(body, T(',').join(ns.var(name)
                for name in arg_names), T(',').join(arg_names))
        body = self.close(ns, body)
        return '(' + args + body + ')'

    def visit_List(self, tree):
        elts = [self.visit(elt) for elt in tree.elts]
        return T('[{}]').format(T(',').join(elts))

    def visit_ListComp(self, tree):
        return T('[{}]').format(T(' ').join([self.visit(tree.elt)] +
                                            map(self.visit, tree.generators)))

    def visit_Name(self, tree):
        return self.var(tree.id)

    def visit_Num(self, tree):
        return T('{!r}').format(tree.n)

    def visit_Pass(self, tree):
        return T('{after}')

    def visit_Print(self, tree):
        to_print = T('{}')
        if tree.dest is not None:
            # Abuse varargs to get the right evaluation order
            to_print = T('file={}, *[{}]').format(self.visit(tree.dest), to_print)
        to_print = to_print.format(T(',').join(self.visit(x) for x in tree.values))
        if not tree.nl:
            # TODO: This is apparently good enough for 2to3, but gets
            # many cases wrong (tests/unimplemented/softspace.py).
            to_print += ", end=' '"
        return T('({__print}({}), {after})[1]').format(to_print)

    def visit_Raise(self, tree):
        if tree.type is None:
            return T('([] for [] in []).throw(*{sys}.exc_info())')
        else:
            return T('([] for [] in []).throw({}{}{})').format(
                self.visit(tree.type),
                '' if tree.inst is None else ', ' + self.visit(tree.inst),
                '' if tree.tback is None else ', ' + self.visit(tree.tback))

    def visit_Repr(self, tree):
        return T('`{}`').format(self.visit(tree.value))

    def visit_Return(self, tree):
        return self.visit(tree.value)

    def visit_Set(self, tree):
        assert tree.elts, '{} is a dict'
        return T('{{{}}}').format(T(', ').join(self.visit(elt) for elt in tree.elts))

    def visit_SetComp(self, tree):
        return self.comprehension_code(
            tree.generators,
            lambda ns, g: T('{{{} {}}}').format(ns.visit(tree.elt), g))

    def visit_Slice(self, tree):
        return T('{}:{}{}').format(
            '' if tree.lower is None else self.visit(tree.lower),
            '' if tree.upper is None else self.visit(tree.upper),
            '' if tree.step is None else ':' + self.visit(tree.step))

    def visit_Str(self, tree):
        return T('{!r}').format(tree.s)

    def visit_Subscript(self, tree):
        return T('{}[{}]').format(self.visit(tree.value), self.visit(tree.slice))

    def visit_TryExcept(self, tree):
        raise NotImplementedError('Open problem: try-except')

    def visit_TryFinally(self, tree):
        raise NotImplementedError('Open problem: try-finally')

    def visit_Tuple(self, tree):
        elts = [self.visit(elt) for elt in tree.elts]
        if len(elts) is 0:
            return T('()')
        elif len(elts) is 1:
            return T('({},)').format(elts[0])
        else:
            return T('({})').format(T(',').join(elts))

    def visit_UnaryOp(self, tree):
        return T('({}{})').format(unaryop_code[type(tree.op)], self.visit(tree.operand))

    def visit_While(self, tree):
        test = self.visit(tree.test)
        body = self.many_to_one(tree.body, after='__this()')
        orelse = self.many_to_one(tree.orelse, after='__after()')
        return lambda_function({'__after': T('lambda: {after}')}).format(
            T('{__y}(lambda __this: lambda: {} if {} else {})()').format(
                provide(body, __break='__after', __continue='__this'),
                test, orelse))

    def visit_With(self, tree):
        raise NotImplementedError('Open problem: with')

    def visit_Yield(self, tree):
        raise NotImplementedError('Open problem: yield')

    def generic_visit(self, tree):
        raise NotImplementedError('Case not caught: %s' % str(type(tree)))


# The entry point for everything.
def to_one_line(original):
    # original :: string
    # :: string
    t = ast.parse(original)
    table = symtable.symtable(original, '<string>', 'exec')

    original = original.strip()

    # If there's only one line anyways, be lazy
    if len(original.splitlines()) == 1 and \
       len(t.body) == 1 and \
       type(t.body[0]) in (ast.Delete, ast.Assign, ast.AugAssign, ast.Print,
                           ast.Raise, ast.Assert, ast.Import, ast.ImportFrom,
                           ast.Exec, ast.Global, ast.Expr, ast.Pass):
        return original

    return get_init_code(Namespace(table).many_to_one(t.body))


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
