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
    if type(tree) is ast.AST:
        pass
    elif type(tree) is ast.Add:
        return '+'
    elif type(tree) is ast.And:
        pass
    elif type(tree) is ast.Assert:
        pass
    elif type(tree) is ast.Assign:
        fi = fields(tree)
        variables = [code(target) for target in fi['targets']]
        value = code(fi['value'])
        if len(variables) is 1:
            variable = variables[0]
            return "(lambda %s: %s)(%s)" % (variable, after, value)
        else:
            raise StandardError("Multiple lefts in an assign not yet supported")
    elif type(tree) is ast.Attribute:
        pass
    elif type(tree) is ast.AugAssign:
        pass
    elif type(tree) is ast.AugLoad:
        pass
    elif type(tree) is ast.AugStore:
        pass
    elif type(tree) is ast.BinOp:
        fi = fields(tree)
        return '(%s%s%s)' % (code(fi['left']), code(fi['op']), code(fi['right']))
    elif type(tree) is ast.BitAnd:
        pass
    elif type(tree) is ast.BitOr:
        pass
    elif type(tree) is ast.BitXor:
        pass
    elif type(tree) is ast.BoolOp:
        pass
    elif type(tree) is ast.Break:
        pass
    elif type(tree) is ast.Call:
        pass
    elif type(tree) is ast.ClassDef:
        pass
    elif type(tree) is ast.Compare:
        pass
    elif type(tree) is ast.Continue:
        pass
    elif type(tree) is ast.Del:
        pass
    elif type(tree) is ast.Delete:
        pass
    elif type(tree) is ast.Dict:
        pass
    elif type(tree) is ast.DictComp:
        pass
    elif type(tree) is ast.Div:
        pass
    elif type(tree) is ast.Ellipsis:
        pass
    elif type(tree) is ast.Eq:
        pass
    elif type(tree) is ast.ExceptHandler:
        pass
    elif type(tree) is ast.Exec:
        pass
    elif type(tree) is ast.Expr:
        pass
    elif type(tree) is ast.Expression:
        pass
    elif type(tree) is ast.ExtSlice:
        pass
    elif type(tree) is ast.FloorDiv:
        pass
    elif type(tree) is ast.For:
        pass
    elif type(tree) is ast.FunctionDef:
        pass
    elif type(tree) is ast.GeneratorExp:
        pass
    elif type(tree) is ast.Global:
        pass
    elif type(tree) is ast.Gt:
        pass
    elif type(tree) is ast.GtE:
        pass
    elif type(tree) is ast.If:
        pass
    elif type(tree) is ast.IfExp:
        pass
    elif type(tree) is ast.Import:
        pass
    elif type(tree) is ast.ImportFrom:
        pass
    elif type(tree) is ast.In:
        pass
    elif type(tree) is ast.Index:
        pass
    elif type(tree) is ast.Interactive:
        pass
    elif type(tree) is ast.Invert:
        pass
    elif type(tree) is ast.Is:
        pass
    elif type(tree) is ast.IsNot:
        pass
    elif type(tree) is ast.LShift:
        pass
    elif type(tree) is ast.Lambda:
        pass
    elif type(tree) is ast.List:
        pass
    elif type(tree) is ast.ListComp:
        pass
    elif type(tree) is ast.Load:
        pass
    elif type(tree) is ast.Lt:
        pass
    elif type(tree) is ast.LtE:
        pass
    elif type(tree) is ast.Mod:
        pass
    elif type(tree) is ast.Module:
        ## Todo: look into sys.stdout instead
        return "from __future__ import print_function; " + many_to_one(child_nodes(tree))
    elif type(tree) is ast.Mult:
        pass
    elif type(tree) is ast.Name:
        return fields(tree)['id']
    elif type(tree) is ast.NodeTransformer:
        pass
    elif type(tree) is ast.NodeVisitor:
        pass
    elif type(tree) is ast.Not:
        pass
    elif type(tree) is ast.NotEq:
        pass
    elif type(tree) is ast.NotIn:
        pass
    elif type(tree) is ast.Num:
        return str(fields(tree)['n'])
    elif type(tree) is ast.Or:
        pass
    elif type(tree) is ast.Param:
        pass
    elif type(tree) is ast.Pass:
        pass
    elif type(tree) is ast.Pow:
        pass
    elif type(tree) is ast.Print:
        to_print = ','.join([code(x) for x in fields(tree)['values']])
        if after is not 'None':
            return "(lambda ___: %s)(print(%s))" % (after, to_print)
        else:
            return "print(%s)" % to_print
    elif type(tree) is ast.PyCF_ONLY_AST:
        pass
    elif type(tree) is ast.RShift:
        pass
    elif type(tree) is ast.Raise:
        pass
    elif type(tree) is ast.Repr:
        pass
    elif type(tree) is ast.Return:
        ## TODO: actually extract value
        return "42"
    elif type(tree) is ast.Set:
        pass
    elif type(tree) is ast.SetComp:
        pass
    elif type(tree) is ast.Slice:
        pass
    elif type(tree) is ast.Store:
        pass
    elif type(tree) is ast.Str:
        pass
    elif type(tree) is ast.Sub:
        pass
    elif type(tree) is ast.Subscript:
        pass
    elif type(tree) is ast.Suite:
        pass
    elif type(tree) is ast.TryExcept:
        pass
    elif type(tree) is ast.TryFinally:
        pass
    elif type(tree) is ast.Tuple:
        pass
    elif type(tree) is ast.UAdd:
        pass
    elif type(tree) is ast.USub:
        pass
    elif type(tree) is ast.UnaryOp:
        pass
    elif type(tree) is ast.While:
        pass
    elif type(tree) is ast.With:
        pass
    elif type(tree) is ast.Yield:
        pass
    else:
        raise StandardError(type(tree))
        

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = sys.argv[0]        

    with open(filename, 'r') as fi:
        source = fi.read()
        t = ast.parse(source)
        print code(t)


"""
            print fields(t)
            if True:
                ooi = fields(t)['body'][2]
                binop = child_nodes(ooi)[1]
                print binop
                print fields(binop)


"""

