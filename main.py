import ast
import sys

def fields(tree):
    return dict(list(ast.iter_fields(tree)))

def child_nodes(tree):
    return list(ast.iter_child_nodes(tree))

def many_to_one(trees):
    # trees :: [Tree]
    # return :: string
    assert type(trees) is list
    if len(trees) is 0:
        return "None"
    else:
        return code_with_after(trees[0], many_to_one(trees[1:]))

def code(tree):
    return code_with_after(tree, "")

def code_with_after(tree, after):
    if type(tree) is ast.Add:
        return '+'
    elif type(tree) is ast.And:
        return ' and '
    elif type(tree) is ast.Assert:
        raise NotImplementedError("Not implemented: assert")
    elif type(tree) is ast.Assign:
        targets = [code(target) for target in tree.targets]
        value = code(tree.value)
        if len(targets) is 1:
            target = targets[0]
            return "(lambda %s: %s)(%s)" % (target, after, value)
        else:
            raise NotImplementedError("Multiple lefts in an assignment")
    elif type(tree) is ast.Attribute:
        return "%s.%s" % (code(tree.value), tree.attr)
    elif type(tree) is ast.AugAssign:
        target = code(tree.target)
        op = code(tree.op)
        value = code(tree.value)
        return "(lambda %s: %s)(%s%s%s)" % (target, after, target, op, value)
    elif type(tree) is ast.AugLoad:
        raise StandardError("AugLoad should not appear in AST")
    elif type(tree) is ast.AugStore:
        raise StandardError("AugStore should not appear in AST")
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
        raise NotImplementedError("Not implemented: break")
    elif type(tree) is ast.Call:
        func = code(tree.func)
        args = [code(arg) for arg in tree.args]
        keywords = [code(kw) for kw in tree.keywords]
        if tree.starargs is None:
            starargs = []
        else:
            starargs = [code(tree.starargs)]
        if tree.kwargs is None:
            kwargs = []
        else:
            kwargs = [code(tree.kwargs)]
        elems = args + keywords + starargs + kwargs
        comma_sep_elems = ','.join(elems)
        return '%s(%s)' % (func, comma_sep_elems)
    elif type(tree) is ast.ClassDef:
        raise NotImplementedError("Not implemented: classdef")
    elif type(tree) is ast.Compare:
        assert len(tree.ops) == len(tree.comparators)
        return code(tree.left) + ''.join([code(tree.ops[i])+code(tree.comparators[i]) for i in range(len(tree.ops))])
    elif type(tree) is ast.Continue:
        raise NotImplementedError("Not implemented: continue")
    elif type(tree) is ast.Del:
        raise NotImplementedError("Not implemented: del")
    elif type(tree) is ast.Delete:
        raise NotImplementedError("Not implemented: delete")
    elif type(tree) is ast.Dict:
        raise NotImplementedError("Not implemented: dict")
    elif type(tree) is ast.DictComp:
        raise NotImplementedError("Not implemented: dict-comp")
    elif type(tree) is ast.Div:
        raise NotImplementedError("Not implemented: div")
    elif type(tree) is ast.Ellipsis:
        raise NotImplementedError("Not implemented: ellipsis")
    elif type(tree) is ast.Eq:
        return '=='
    elif type(tree) is ast.ExceptHandler:
        raise NotImplementedError("Not implemented: except")
    elif type(tree) is ast.Exec:
        raise NotImplementedError("Not implemented: exec")
    elif type(tree) is ast.Expr:
        code_to_exec = code(tree.value)
        if after is not 'None':
            return "(lambda ___: %s)(%s)" % (after, code_to_exec)
        else:
            return "%s" % code_to_exec
    elif type(tree) is ast.Expression:
        raise NotImplementedError("Not implemented: expression")
    elif type(tree) is ast.ExtSlice:
        raise NotImplementedError("Not implemented: extslice")
    elif type(tree) is ast.FloorDiv:
        raise NotImplementedError("Not implemented: floordiv")
    elif type(tree) is ast.For:
        raise NotImplementedError("Not implemented: for")
    elif type(tree) is ast.FunctionDef:
        raise NotImplementedError("Not implemented: functiondef")
    elif type(tree) is ast.GeneratorExp:
        raise NotImplementedError("Not implemented: generatorexp")
    elif type(tree) is ast.Global:
        raise NotImplementedError("Not implemented: global")
    elif type(tree) is ast.Gt:
        return '>'
    elif type(tree) is ast.GtE:
        return '>='
    elif type(tree) is ast.If:
        raise NotImplementedError("Not implemented: if")
    elif type(tree) is ast.IfExp:
        raise NotImplementedError("Not implemented: ifexp")
    elif type(tree) is ast.Import:
        raise NotImplementedError("Not implemented: import")
    elif type(tree) is ast.ImportFrom:
        raise NotImplementedError("Not implemented: importfrom")
    elif type(tree) is ast.In:
        return " in "
    elif type(tree) is ast.Index:
        return '[%s]' % code(tree.value)
    elif type(tree) is ast.Interactive:
        raise NotImplementedError("Not implemented: interactive")
    elif type(tree) is ast.Invert:
        return "~"
    elif type(tree) is ast.Is:
        return ' is '
    elif type(tree) is ast.IsNot:
        return ' is not '
    elif type(tree) is ast.LShift:
        return '<<'
    elif type(tree) is ast.keyword:
        return '%s=%s' % (tree.arg, code(tree.value))
    elif type(tree) is ast.Lambda:
        raise NotImplementedError("Not implemented: lambda")
    elif type(tree) is ast.List:
        raise NotImplementedError("Not implemented: list")
    elif type(tree) is ast.ListComp:
        raise NotImplementedError("Not implemented: listcomp")
    elif type(tree) is ast.Load:
        raise NotImplementedError("Not implemented: load")
    elif type(tree) is ast.Lt:
        return '<'
    elif type(tree) is ast.LtE:
        return '<='
    elif type(tree) is ast.Mod:
        return '%'
    elif type(tree) is ast.Module:
        ## Todo: look into sys.stdout instead
        return "from __future__ import print_function; " + many_to_one(child_nodes(tree))
    elif type(tree) is ast.Mult:
        return '*'
    elif type(tree) is ast.Name:
        return tree.id
    elif type(tree) is ast.NodeTransformer:
        raise NotImplementedError("Not implemented: nodetransformer")
    elif type(tree) is ast.NodeVisitor:
        raise NotImplementedError("Not implemented: nodevisitor")
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
    elif type(tree) is ast.Param:
        raise NotImplementedError("Not implemented: param")
    elif type(tree) is ast.Pass:
        return after
    elif type(tree) is ast.Pow:
        return '**'
    elif type(tree) is ast.Print:
        to_print = ','.join([code(x) for x in tree.values])
        if after is not 'None':
            return "(lambda ___: %s)(print(%s))" % (after, to_print)
        else:
            return "print(%s)" % to_print
    elif type(tree) is ast.PyCF_ONLY_AST:
        raise NotImplementedError("Not implemented: pycf only ast")
    elif type(tree) is ast.RShift:
        return '>>'
    elif type(tree) is ast.Raise:
        raise NotImplementedError("Not implemented: raise")
    elif type(tree) is ast.Repr:
        raise NotImplementedError("Not implemented: repr")
    elif type(tree) is ast.Return:
        ## TODO: actually extract value
        return "42"
    elif type(tree) is ast.Set:
        raise NotImplementedError("Not implemented: set")
    elif type(tree) is ast.SetComp:
        raise NotImplementedError("Not implemented: setcomp")
    elif type(tree) is ast.Slice:
        raise NotImplementedError("Not implemented: slice")
    elif type(tree) is ast.Store:
        raise NotImplementedError("Not implemented: store")
    elif type(tree) is ast.Str:
        return repr(tree.s)
    elif type(tree) is ast.Sub:
        return '-'
    elif type(tree) is ast.Subscript:
        raise NotImplementedError("Not implemented: subscript")
    elif type(tree) is ast.Suite:
        raise NotImplementedError("Not implemented: suite")
    elif type(tree) is ast.TryExcept:
        raise NotImplementedError("Not implemented: try-except")
    elif type(tree) is ast.TryFinally:
        raise NotImplementedError("Not implemented: try-finally")
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
        return "(%s%s)" % (code(tree.op), code(tree.operand))
    elif type(tree) is ast.While:
        raise NotImplementedError("Not implemented: while")
    elif type(tree) is ast.With:
        raise NotImplementedError("Not implemented: with")
    elif type(tree) is ast.Yield:
        raise NotImplementedError("Not implemented: yield")
    else:
        raise NotImplementedError("Case not caught: %s" % str(type(tree)))
        

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = sys.argv[0]        

    with open(filename, 'r') as fi:
        original = fi.read()
        t = ast.parse(original)
        print "---------- ORIGINAL ----------"
        print original
        onelined = code(t)
        print "---------- ONELINED ----------"
        print onelined

        print "TESTING RESULTS: original/onelined"
        try:
            exec(original)
        except Exception as e:
            print e
        try:
            exec(onelined)
        except Exception as e:
            print e
