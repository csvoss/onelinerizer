"""Convert any Python file into a single line of code.

Usage via the command line:

$ python main.py --help
    print usages
$ python main.py infile.py
    one-line infile.py, put the result in infile.ol.py
$ python main.py infile.py outfile.py
    one-line infile.py, put the result in outfile.py
"""

import ast
import symtable
import traceback

from .template import T


def lambda_function(arguments_to_values):
    """
    Arguments:
        arguments_to_values: {string: string | T} - e.g. {'a': '47'}

    Returns:
        T - e.g. (lambda a: {})(47)
    """
    return T('(lambda {}: {})({})').format(
        T(', ').join(arguments_to_values.keys()),
        T('{}'),
        T(', ').join(arguments_to_values.values()))

def provide(body, **subs):
    """
    Provide the variables in subs to the code in `body`, by wrapping
    `body` in a lambda function if needed.

    Arguments:
        body: string | T, e.g. '__print(42)'
        subs: {string: string | T}, e.g. {'__print': 'f'}

    Returns:
        T - e.g. (lambda __print: __print(42))(f)
    """
    body = T('{}').format(body)
    needed = set(body.free()).intersection(subs)
    if needed:
        return lambda_function({k: subs[k] for k in needed}).format(
            body.format(**{k: k for k in needed}))
    else:
        return body


def get_init_code(tree, table):
    """Get one-lined code from `tree` and `table.

    Calculate the helper variables that we will need, and wrap the output
    code (computed from `tree`) with definitions of those variables.

    TODO: Short-circuit to something far simpler if the program has only one
    print statement.

    Arguments:
        tree: Python AST node
        table: symtable.symtable

    Returns:
        string - valid one-line code
    """
    output = Namespace(table).many_to_one(tree.body)

    doc = ast.get_docstring(tree, clean=False)
    if doc is not None:
        output = assignment_component(output, T("{__g}['__doc__']"), repr(doc))

    output = provide(
        output.format(__l=T('{__g}')),
        __print=T("__import__('__builtin__', level=0).__dict__['print']"),
        __y="(lambda f: (lambda x: x(x))(lambda y:"
          " f(lambda: y(y)())))",
        __g=T("globals()"),
        __contextlib="__import__('contextlib', level=0)",
        __operator="__import__('operator', level=0)",
        __sys="__import__('sys', level=0)",
        __types="__import__('types', level=0)")

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
    ast.Eq: ' == ',
    ast.NotEq: ' != ',
    ast.Lt: ' < ',
    ast.LtE: ' <= ',
    ast.Gt: ' > ',
    ast.GtE: ' >= ',
    ast.Is: ' is ',
    ast.IsNot: ' is not ',
    ast.In: ' in ',
    ast.NotIn: ' not in ',
}


def assignment_component(after, targets, value):
    """
    Assign `targets` to `value` in the code `after`.

    Arguments:
        after: string, e.g. 'x+42'
        targets: string, e.g. 'x,y,z'
        value: string, e.g. '(1,2,3)'

    Returns:
        T, e.g. T('[x+42 for x,y,z in [((1,2,3))]]')
    """
    # Old way:
    # return T('(lambda {}: {})({})').format(targets, after, value)
    return T('[{} for {} in [({})]][0]').format(after, targets, value)


class Namespace(ast.NodeVisitor):
    """
    AST visitor.
    """
    def __init__(self, table, private=''):
        self.table = table
        self.subtables = iter(table.get_children())
        self.private = '_' + table.get_name() if table.get_type() == 'class' \
                       else private
        self.futures = set()

    def next_child(self):
        return Namespace(next(self.subtables), private=self.private)

    def mangle(self, name):
        return self.private + name if name.startswith('__') and \
            not name.endswith('__') else name

    def var(self, name):
        name = self.mangle(name)
        sym = self.table.lookup(name)
        if self.table.get_type() == 'module' or (sym.is_global() and self.table.is_optimized()) or name == 'None':
            return T('{__print}') if name == 'print' else T('{}').format(name)
        elif sym.is_global():
            return T('({__l}[{!r}] if {!r} in __l else {})').format(
                name, name, T('{__print}') if name == 'print' else name)
        elif sym.is_local():
            return T('{__l}[{!r}]').format(name)
        elif sym.is_free():
            return T('{___f_' + name + '}()').format(name)
        else:
            raise SyntaxError('confusing symbol {!r}'.format(name))

    def store_var(self, name):
        name = self.mangle(name)
        sym = self.table.lookup(name)
        if sym.is_global():
            return T('{__g}[{!r}]').format(name)
        elif sym.is_local():
            return T('{__l}[{!r}]').format(name)
        elif sym.is_free():
            raise SyntaxError('storing free variable {!r}'.format(name))
        else:
            raise SyntaxError('confusing symbol {!r}'.format(name))

    def delete_var(self, name):
        name = self.mangle(name)
        sym = self.table.lookup(name)
        if sym.is_global():
            return T('{__g}.pop({!r})').format(name)
        elif sym.is_local():
            return T('{__l}.pop({!r})').format(name)
        elif sym.is_free():
            raise SyntaxError('deleting free variable {!r}'.format(name))
        else:
            raise SyntaxError('confusing symbol {!r}'.format(name))

    def close(self, ns, local, body, **subs):
        if self.table.get_type() == 'function':
            subs = dict(subs, **{'___f_' + v: T('lambda: {}').format(self.var(v))
                                 for v in self.table.get_locals()})
        return provide(body, __l=local, **subs)

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
            return T('({})').format(T(', ').join(map(self.slice_repr, slice.dims)) +
                                    ','*(len(slice.dims) == 1))
        elif type(slice) is ast.Index:
            return self.visit(slice.value)
        else:
            raise NotImplementedError('Case not caught: %s' % str(type(slice)))

    def delete_code(self, target):
        if type(target) is ast.Attribute:
            return [T('delattr({}, {!r})').format(self.visit(target.value), target.attr)]
        elif type(target) is ast.Subscript:
            if type(target.slice) is ast.Slice and target.slice.step is None:
                return [T("(lambda o, **t: type('translator', (), {{t[m]: "
                          "staticmethod(object.__getattribute__(d[m], '__get__'"
                          ")(o, type(o))) for d in [object.__getattribute__("
                          "type(o), '__dict__')] for m in t if m in d}})())({},"
                          " __delitem__='__getitem__', __delslice__="
                          "'__getslice__', __len__='__len__')[{}]").format(
                              self.visit(target.value),
                              self.visit(target.slice))]
            else:
                return [T("{__operator}.delitem({}, {})").format(
                    self.visit(target.value),
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
        targets = T(', ').join(targets)
        return assignment_component(T('{after}'), targets,
            value if len(tree.targets) == 1
                  else T('[{}]*{}').format(value, len(tree.targets)))

    def visit_Attribute(self, tree):
        return T('{}.{}').format(self.visit(tree.value), tree.attr)

    def visit_AugAssign(self, tree):
        if type(tree.target) is ast.Attribute:
            target_params = ['__target']
            target_args = [self.visit(tree.target.value)]
            target_value = T('__target.{}').format(tree.target.attr)
        elif type(tree.target) is ast.Subscript:
            if type(tree.target.slice) is ast.Slice and tree.target.slice.step is None:
                target_params = ['__target']
                target_args = [self.visit(tree.target.value)]
                if tree.target.slice.lower is not None:
                    target_params.append('__lower')
                    target_args.append(self.visit(tree.target.slice.lower))
                if tree.target.slice.upper is not None:
                    target_params.append('__upper')
                    target_args.append(self.visit(tree.target.slice.upper))
                target_value = T('__target[{}:{}]').format(
                    '' if tree.target.slice.lower is None else '__lower',
                    '' if tree.target.slice.upper is None else '__upper')
            else:
                target_params = ['__target', '__slice']
                target_args = [self.visit(tree.target.value), self.slice_repr(tree.target.slice)]
                target_value = '__target[__slice]'
        elif type(tree.target) is ast.Name:
            target_params = []
            target_args = []
            target_value = self.store_var(tree.target.id)
        else:
            raise SyntaxError('illegal expression for augmented assignment')

        iop = type(tree.op).__name__.lower()
        if iop.startswith('bit'):
            iop = iop[len('bit'):]
        if 'division' in self.futures and isinstance(tree.op, ast.Div):
            iop = 'truediv'
        value = self.visit(tree.value)
        assign = assignment_component(
            T('{after}'), target_value,
            T("{__operator}.i{}({}, {})").format(iop, target_value, value))
        if target_params:
            assign = T('(lambda {}: {})({})').format(
                T(', ').join(target_params),
                assign,
                T(', ').join(target_args))
        return assign

    def visit_BinOp(self, tree):
        if 'division' in self.futures and isinstance(tree.op, ast.Div):
            return T('{__operator}.truediv({}, {})').format(self.visit(tree.left), self.visit(tree.right))
        return T('({} {} {})').format(self.visit(tree.left), operator_code[type(tree.op)], self.visit(tree.right))

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
        comma_sep_elems = T(', ').join(elems)
        return T('{}({})').format(func, comma_sep_elems)

    def visit_ClassDef(self, tree):
        bases = (T(', ').join(map(self.visit, tree.bases)) +
                 ','*(len(tree.bases) == 1))
        decoration = T('{}')
        for decorator in tree.decorator_list:
            decoration = decoration.format(T('{}({})').format(self.visit(decorator), T('{}')))
        ns = self.next_child()
        body = ns.many_to_one(tree.body, after=T('{__l}'))
        doc = ast.get_docstring(tree, clean=False)
        body = self.close(ns, "{{'__module__': __name__{}}}".format(
            '' if doc is None else ", '__doc__': {!r}".format(doc)), body)
        if tree.bases:
            class_code = T("(lambda b, d: d.get('__metaclass__', getattr(b[0], "
                           "'__class__', type(b[0])))({!r}, b, d))(({}), "
                           "{})").format(tree.name, bases, body)
        else:
            class_code = T("(lambda d: d.get('__metaclass__', {__g}.get("
                           "'__metaclass__', {__types}.ClassType))({!r}, (), "
                           "d))({})").format(tree.name, body)
        class_code = decoration.format(class_code)
        return assignment_component(T('{after}'), self.store_var(tree.name), class_code)

    def visit_Compare(self, tree):
        assert len(tree.ops) == len(tree.comparators)
        return T('({})').format(self.visit(tree.left) + T('').join(
            [cmpop_code[type(tree.ops[i])] + self.visit(tree.comparators[i])
             for i in range(len(tree.ops))]))

    def visit_comprehension(self, tree):
        return (T('for {} in {}').format(self.visit(tree.target), self.visit(tree.iter)) +
                T('').join(' if ' + self.visit(i) for i in tree.ifs))

    def comprehension_code(self, generators, wrap):
        iter0 = self.visit(generators[0].iter)
        ns = self.next_child()
        return self.close(
            ns, '{}',
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
        return T('{{{}}}').format(T(', ').join(
            T('{}: {}').format(k, v)
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
        if tree.globals is None and self.table.get_type() == 'module':
            exec_code = T(
                "eval(compile({}, '<string>', 'exec'), "
                "None, {__l})").format(body)
        elif tree.globals is None:
            exec_code = T(
                "(lambda b, c: (eval(compile(b, '<string>', 'exec'), "
                "None, c), {__l}.update(c)))({}, {__l}.copy())").format(body)
        elif tree.locals is None and self.table.get_type() == 'module':
            exec_code = T(
                "(lambda b, g: eval(compile(b, '<string>', 'exec'), g, "
                "{__l} if g is None else g))({}, {})").format(
                    body, self.visit(tree.globals))
        elif tree.locals is None:
            exec_code = T(
                "(lambda b, g, c: (eval(compile(b, '<string>', 'exec'), g, "
                "c if g is None else g), "
                "{__l}.update(c)))({}, {}, {__l}.copy())").format(
                    body, self.visit(tree.globals))
        elif self.table.get_type() == 'module':
            exec_code = T(
                "(lambda b, g, l: eval(compile(b, '<string>', 'exec'), g, "
                "({__l} if g is None else g) if l is None "
                "else l))({}, {}, {})").format(
                    body, self.visit(tree.globals), self.visit(tree.locals))
        else:
            exec_code = T(
                "(lambda b, g, l, c: (eval(compile(b, '<string>', 'exec'), g, "
                "(c if g is None else g) if l is None else l), "
                "{__l}.update(c)))({}, {}, {}, {__l}.copy())").format(
                    body, self.visit(tree.globals), self.visit(tree.locals))
        return T('({}, {after})[1]').format(exec_code)

    def visit_Expr(self, tree):
        return T('({}, {after})[1]').format(self.visit(tree.value))

    def visit_Expression(self, tree):
        return self.visit(tree.body)

    def visit_ExtSlice(self, tree):
        return (T(', ').join(map(self.visit, tree.dims)) +
                ','*(len(tree.dims) == 1))

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
        # ('lambda x, y, z=5, *args: ', ['x', 'y', 'z', 'args'])
        args, arg_names = self.visit(tree.args)
        decoration = T('{}')
        for decorator in tree.decorator_list:
            decoration = decoration.format(T('{}({})').format(self.visit(decorator), T('{}')))
        ns = self.next_child()
        body = ns.many_to_one(tree.body).format(pre_return='', post_return='')
        if arg_names:
            body = assignment_component(body,
                T(', ').join(ns.var(name) for name in arg_names),
                T(', ').join(arg_names))
        body = self.close(ns, '{}', body)
        function_code = args + body
        doc = ast.get_docstring(tree, clean=False)
        if tree.decorator_list:
            return assignment_component(
                T('{after}'),
                self.store_var(tree.name),
                decoration.format(assignment_component(
                    '__func',
                    '__func, __func.__name__' + ('' if doc is None else ', __func.__doc__'),
                    T('{}, {!r}' + ('' if doc is None else ', {!r}')).format(
                        function_code, tree.name, doc))))
        else:
            return assignment_component(
                T('{after}'),
                T('{}, {}.__name__' + ('' if doc is None else ', {}.__doc__')).format(
                    self.store_var(tree.name), self.var(tree.name), self.var(tree.name)),
                T('{}, {!r}' + ('' if doc is None else ', {!r}')).format(
                    function_code, tree.name, doc))

    def visit_arguments(self, tree):
        # this should return something of the form
        # ('lambda x, y, z=5, *args: ', ['x', 'y', 'z', 'args'])
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
        args = T(', ').join(args)
        return (T('lambda {}: ').format(args), arg_names)

    def visit_GeneratorExp(self, tree):
        return self.comprehension_code(
            tree.generators,
            lambda ns, g: T('({} {})').format(ns.visit(tree.elt), g))

    def visit_Global(self, tree):
        return T('{after}')

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
        level_arg = ', level=0' if 'absolute_import' in self.futures else ''
        for alias in tree.names:
            ids = alias.name.split('.')
            if alias.asname is None:
                after = assignment_component(after, self.store_var(ids[0]),
                    T('__import__({!r}, {__g}, {__l}{})').format(
                        alias.name, level_arg))
            else:
                after = assignment_component(after, self.store_var(alias.asname),
                    T('.').join([T('__import__({!r}, {__g}, {__l}{})').format(
                        alias.name, level_arg)] + ids[1:]))
        return after

    def visit_ImportFrom(self, tree):
        body = assignment_component(
            T('{after}'),
            T(', ').join(self.store_var(alias.name if alias.asname is None
                                        else alias.asname) for alias in tree.names),
            T(', ').join('__mod.' + alias.name for alias in tree.names))
        if tree.module == '__future__':
            self.futures |= set(alias.name for alias in tree.names)
            body = T(
                '(lambda __f: type(__f)(type(__f.func_code)('
                '__f.func_code.co_argcount, '
                '__f.func_code.co_nlocals, '
                '__f.func_code.co_stacksize, '
                '__f.func_code.co_flags{}, '
                '__f.func_code.co_code, '
                '__f.func_code.co_consts, '
                '__f.func_code.co_names, '
                '__f.func_code.co_varnames, '
                '__f.func_code.co_filename, '
                '__f.func_code.co_name, '
                '__f.func_code.co_firstlineno, '
                '__f.func_code.co_lnotab, '
                '__f.func_code.co_freevars, '
                '__f.func_code.co_cellvars), '
                '__f.func_globals, '
                '__f.func_name, '
                '__f.func_defaults, '
                '__f.func_closure)())(lambda: {})'
            ).format(
                ''.join(' | __mod.' + alias.name + '.compiler_flag'
                        for alias in tree.names),
                body)
        return T('(lambda __mod: {})(__import__({!r}, {__g}, {__l},'
                 ' {!r}, {!r}))').format(
            body,
            '' if tree.module is None else tree.module,
            tuple(alias.name for alias in tree.names),
            tree.level)

    def visit_Index(self, tree):
        return self.visit(tree.value)

    def visit_keyword(self, tree):
        return T('{}={}').format(tree.arg, self.visit(tree.value))

    def visit_Lambda(self, tree):
        args, arg_names = self.visit(tree.args)
        ns = self.next_child()
        body = ns.visit(tree.body)
        if arg_names:
            body = assignment_component(body, T(', ').join(ns.store_var(name)
                for name in arg_names), T(', ').join(arg_names))
        body = self.close(ns, '{}', body)
        return '(' + args + body + ')'

    def visit_List(self, tree):
        elts = [self.visit(elt) for elt in tree.elts]
        return T('[{}]').format(T(', ').join(elts))

    def visit_ListComp(self, tree):
        return T('[{}]').format(T(' ').join([self.visit(tree.elt)] +
                                            map(self.visit, tree.generators)))

    def visit_Name(self, tree):
        if isinstance(tree.ctx, (ast.Store, ast.AugStore)):
            return self.store_var(tree.id)
        else:
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
        to_print = to_print.format(T(', ').join(self.visit(x) for x in tree.values))
        if not tree.nl:
            # TODO: This is apparently good enough for 2to3, but gets
            # many cases wrong (tests/unimplemented/softspace.py).
            to_print += ", end=' '"
        return T('({__print}({}), {after})[1]').format(to_print)

    def visit_Raise(self, tree):
        if tree.type is None:
            return T('([] for [] in []).throw(*{__sys}.exc_info())')
        else:
            return T('([] for [] in []).throw({}{}{})').format(
                self.visit(tree.type),
                '' if tree.inst is None else ', ' + self.visit(tree.inst),
                '' if tree.tback is None else ', ' + self.visit(tree.tback))

    def visit_Repr(self, tree):
        return T('`{}`').format(self.visit(tree.value))

    def visit_Return(self, tree):
        return T('{pre_return}{}{post_return}').format(
            'None' if tree.value is None else self.visit(tree.value))

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
        body = self.many_to_one(
            tree.body, after=T('(lambda __after: {orelse})')).format(
                orelse=self.many_to_one(tree.orelse, after='__after()'),
                pre_return=T('(lambda ret: lambda after: ret)({pre_return}'),
                post_return=T('{post_return})'))
        handlers = []
        for handler in tree.handlers:
            if handler.type is None:
                code = T('{body}')
            else:
                code = T('issubclass(__exctype, {type}) and {body}').format(
                    type=self.visit(handler.type))
            if handler.name is not None:
                code = code.format(body=assignment_component(
                    T('{body}'), self.visit(handler.name), '__value'))
            handlers.append(code.format(
                body=assignment_component(
                    'True',
                    '__out[0]',
                    self.many_to_one(handler.body, after='lambda after: after()').format(
                        pre_return=T('(lambda ret: lambda after: ret)({pre_return}'),
                        post_return=T('{post_return})')))))
        return \
            lambda_function({'__out': '[None]'}).format(
                lambda_function({
                    '__ctx': T(
                        "{__contextlib}.nested(type('except', (), {{"
                        "'__enter__': lambda self: None, "
                        "'__exit__': lambda __self, __exctype, __value, __traceback: "
                        "__exctype is not None and ({handlers})}})(), "
                        "type('try', (), {{"
                        "'__enter__': lambda self: None, "
                        "'__exit__': lambda __self, __exctype, __value, __traceback: "
                        "{body}}})())").format(
                            body=assignment_component('False', '__out[0]', body),
                            handlers=T(' or ').join(handlers))
                }).format(
                    T('[__ctx.__enter__(), __ctx.__exit__(None, None, None), __out[0](lambda: {after})][2]')))

    def visit_TryFinally(self, tree):
        body = self.many_to_one(
            tree.body, after=T('(lambda after: after())')).format(
                pre_return=T('(lambda ret: lambda after: ret)({pre_return}'),
                post_return=T('{post_return})'))

        finalbody = self.many_to_one(tree.finalbody, after=T('{after}'))
        if 'pre_return' in finalbody.free():
            finalbody = T('({})(lambda ret: {})').format(
                finalbody.format(
                    after='lambda change_ret: False',
                    pre_return=T('(lambda ret: lambda change_ret: change_ret(ret))({pre_return}'),
                    post_return=T('{post_return})')),
                assignment_component('True', '__out[0]', 'lambda after: ret'))
        else:
            finalbody = finalbody.format(after='False')

        return \
            lambda_function({'__out': '[None]'}).format(
                lambda_function({
                    '__ctx': T(
                        "{__contextlib}.nested(type('except', (), {{"
                        "'__enter__': lambda self: None, "
                        "'__exit__': lambda __self, __exctype, __value, __traceback: "
                        "{finalbody}}})(), "
                        "type('try', (), {{"
                        "'__enter__': lambda self: None, "
                        "'__exit__': lambda __self, __exctype, __value, __traceback: "
                        "{body}}})())").format(
                            body=assignment_component('False', '__out[0]', body),
                            finalbody=finalbody)
                }).format(
                    T('[__ctx.__enter__(), __ctx.__exit__(None, None, None), __out[0](lambda: {after})][2]')))

    def visit_Tuple(self, tree):
        return T('({})').format(T(', ').join(map(self.visit, tree.elts)) +
                                ','*(len(tree.elts) == 1))

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
def onelinerize(original):
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

    return get_init_code(t, table)
