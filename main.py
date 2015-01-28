import ast
import sys


INIT_CODE = "(lambda __builtin__: (lambda __print, d: %s)(__builtin__.__dict__['print'],type('',(),{})))(__import__('__builtin__'))"

def fields(tree):
    return dict(list(ast.iter_fields(tree)))

def child_nodes(tree):
    return list(ast.iter_child_nodes(tree))

def many_to_one(trees):
    # trees :: [Tree]
    # return :: string
    assert type(trees) is list
    if len(trees) is 0:
        return 'None'
    else:
        return code_with_after(trees[0], many_to_one(trees[1:]))

def code(tree):
    return code_with_after(tree, 'None')

def code_with_after(tree, after):
    if type(tree) is ast.Add:
        return '+'
    elif type(tree) is ast.And:
        return ' and '
    elif type(tree) is ast.Assert:
        raise NotImplementedError('Open problem (intractable?): assert')
    elif type(tree) is ast.Assign:
        targets = [code(target) for target in tree.targets]
        value = code(tree.value)
        targets = ','.join(targets)
        return '[%s for %s in [(%s)]][0]' % (after, targets, value)
    elif type(tree) is ast.Attribute:
        return '%s.%s' % (code(tree.value), tree.attr)
    elif type(tree) is ast.AugAssign:
        target = code(tree.target)
        op = code(tree.op)
        value = code(tree.value)
        return '[%s for %s in [%s%s%s]][0]' % (after, target, target, op, value)
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
        raise NotImplementedError('TODO: break')
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
        raise NotImplementedError('Open problem: classdef')
        ## Note to self: delattr and setattr are useful things
        ## also you're DEFINITELY going to want this:
        ## https://docs.python.org/2/library/functions.html#type
    elif type(tree) is ast.Compare:
        assert len(tree.ops) == len(tree.comparators)
        return code(tree.left) + ''.join([code(tree.ops[i])+code(tree.comparators[i]) for i in range(len(tree.ops))])
    elif type(tree) is ast.comprehension:
        return ('for %s in %s' % (code(tree.target), code(tree.iter))) + ''.join([' if '+code(i) for i in tree.ifs])
    elif type(tree) is ast.Continue:
        raise NotImplementedError('TODO: continue')
    elif type(tree) is ast.Delete:
        raise NotImplementedError('Open problem: delete')
        ## Note also: globals() and locals() are useful here
    elif type(tree) is ast.Dict:
        return '{%s}' % ','.join([('%s:%s'%(code(k), code(v))) for (k,v) in zip(tree.keys, tree.values)])
    elif type(tree) is ast.DictComp:
        return '{%s}' % (' '.join([code(tree.key)+":"+code(tree.value)] + [code(gen) for gen in tree.generators]))
    elif type(tree) is ast.Div: ## TODO -- no from future division
        return '/'
    elif type(tree) is ast.Ellipsis:
        return '...'
    elif type(tree) is ast.Eq:
        return '=='
    elif type(tree) is ast.ExceptHandler:
        raise NotImplementedError('Open problem (intractable?): except')
    elif type(tree) is ast.Exec:
        raise NotImplementedError('TODO: exec')
    elif type(tree) is ast.Expr:
        code_to_exec = code(tree.value)
        return '(lambda ___: %s)(%s)' % (after, code_to_exec) ## TODO: ensure ___ isn't taken
    elif type(tree) is ast.Expression:
        return code(tree.body)
    elif type(tree) is ast.ExtSlice:
        return ', '.join([code(dim) for dim in tree.dims])
    elif type(tree) is ast.FloorDiv:
        return '//'
    elif type(tree) is ast.For:
        raise NotImplementedError('TODO: for')
    elif type(tree) is ast.FunctionDef:
        args, arg_names = code(tree.args) ## of the form ('lambda x, y, z=5, *args:', ['x','y','z','args'])
        body = many_to_one(tree.body)
        body = '[%s for %s in [(%s)]][0]' % (body, 'd.'+',d.'.join(arg_names), ','.join(arg_names)) ## apply lets for d.arguments
        function_code = args + body
        if len(tree.decorator_list) > 0:
            for decorator in tree.decorator_list:
                function_code = "%s(%s)" % (code(decorator), function_code)
        return "(lambda %s: %s)(%s)" % (tree.name, after, function_code)
    elif type(tree) is ast.arguments:
        ## return something of the form ('lambda x, y, z=5, *args:', ['x','y','z','args'])
        padded_defaults = [None]*(len(tree.args)-len(tree.defaults)) + tree.defaults
        arg_names = [arg.id for arg in tree.args]
        args = zip(padded_defaults, tree.args)
        args = [a.id if d is None else a.id+"="+code(d) for (d,a) in args] ## TODO: str or code?
        if tree.vararg is not None:
            args += ["*" + tree.vararg]
            arg_names += [tree.vararg]
        if tree.kwarg is not None:
            args += ["**" + tree.kwarg]
            arg_names += [tree.kwarg]
        args = ",".join(args)
        return ("lambda %s:" % (args), arg_names)
    elif type(tree) is ast.GeneratorExp:
        raise NotImplementedError('TODO: generatorexp')
    elif type(tree) is ast.Global:
        raise NotImplementedError('Open problem: global')
    elif type(tree) is ast.Gt:
        return '>'
    elif type(tree) is ast.GtE:
        return '>='
    elif type(tree) is ast.If:
        raise NotImplementedError('TODO: if')
    elif type(tree) is ast.IfExp:
        return "(%s if %s else %s)" % (code(tree.body), code(tree.test), code(tree.orelse))
    elif type(tree) is ast.Import:
        for alias in tree.names:
            if alias.asname is None:
                alias.asname = alias.name
            after = "(lambda %s: %s)(__import__('%s'))" % (alias.asname, after, alias.name)
        return after
    elif type(tree) is ast.ImportFrom:
        raise NotImplementedError('Open problem:: importfrom')
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
        body = '[%s for %s in [(%s)]][0]' % (body, 'd.'+',d.'.join(arg_names), ','.join(arg_names)) ## apply lets for d.arguments
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
        return tree.id
    elif type(tree) is ast.Not:
        return 'not '
    elif type(tree) is ast.NotEq:
        return '!='
    elif type(tree) is ast.NotIn:
        return ' not in '
    elif type(tree) is ast.Num:
        return str(tree.n)
    elif type(tree) is ast.Or:
        return ' or '
    elif type(tree) is ast.Pass:
        return after
    elif type(tree) is ast.Pow:
        return '**'
    elif type(tree) is ast.Print:
        to_print = ','.join([code(x) for x in tree.values])
        if after is not 'None':
            return '(lambda ___: %s)(__print(%s))' % (after, to_print) ## TODO: ensure ___ isn't taken
        else:
            return '__print(%s)' % to_print
    elif type(tree) is ast.RShift:
        return '>>'
    elif type(tree) is ast.Raise:
        raise NotImplementedError('Open problem (intractable?): raise')
    elif type(tree) is ast.Repr:
        return 'repr(%s)' % code(tree.value)
    elif type(tree) is ast.Return:
        return code(tree.value)
    elif type(tree) is ast.Set:
        return 'set(%s)' % tree.elts
    elif type(tree) is ast.SetComp:
        return '{%s}' % (' '.join([code(tree.elt)] + [code(gen) for gen in tree.generators]))
    elif type(tree) is ast.Slice:
        if tree.step is None:
            return '%s:%s' % (code(tree.lower), code(tree.upper))
        else:
            return '%s:%s:%s' % (code(tree.lower), code(tree.upper), code(tree.step))
    elif type(tree) is ast.Str:
        return repr(tree.s)
    elif type(tree) is ast.Sub:
        return '-'
    elif type(tree) is ast.Subscript:
        return '%s[%s]' % (code(tree.value), code(tree.slice))
    elif type(tree) is ast.Suite:
        return INIT_CODE % many_to_one(child_nodes(tree))
    elif type(tree) is ast.TryExcept:
        raise NotImplementedError('Open problem (intractable?): try-except')
    elif type(tree) is ast.TryFinally:
        raise NotImplementedError('Open problem (intractable?): try-finally')
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
        raise NotImplementedError('TODO: while')
    elif type(tree) is ast.With:
        raise NotImplementedError('Open problem: with')
    elif type(tree) is ast.Yield:
        raise NotImplementedError('Open problem: yield')
    else:
        raise NotImplementedError('Case not caught: %s' % str(type(tree)))

def to_one_line(original):
    t = ast.parse(original)
    return code(t)

VERBOSE = True ## TODO: Use command line arg instead

if __name__ == '__main__':

    ## TODO: Put the output in a new file instead of just printing like this.

    try:
        filename = sys.argv[1]
    except IndexError:
        print "Usage: python main.py filename" # TODO: stderr instead
    try:
        with open(filename, 'r') as fi:
            if VERBOSE:
                original = fi.read().strip()
                onelined = to_one_line(original)

                print '--- ORIGINAL ---------------------------------'
                print original
                print '----------------------------------------------'
                try:
                    exec(original)
                except Exception as e:
                    print e
                print ''
                print '--- ONELINED ---------------------------------'
                print onelined
                print '----------------------------------------------'
                try:
                    exec(onelined)
                except Exception as e:
                    print e
            else:
                raise NotImplementedError("Non-testing functionality")
    except IOError:
        print "Input file not found: %s" % filename  # TODO: stderr instead

