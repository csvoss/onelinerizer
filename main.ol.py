(lambda __builtin__: (lambda __print, __y, __d: [[[[[[[[[[(lambda __after: (lambda __after: (lambda ___: __after(__d))(__print('Usage: python main.py inputfilename [outputfilename]')) if __d.len(__d.sys.argv)<=1 else [__after(__d) for __d.infilename in [(__d.sys.argv[1])]][0])(lambda __d: (lambda __after: [__after(__d) for __d.outfilename in [(__d.sys.argv[2])]][0] if __d.len(__d.sys.argv)>=3 else (lambda __after: [__after(__d) for __d.outfilename in [('.ol.py'.join(__d.infilename.rsplit('.py',1)))]][0] if '.py' in __d.infilename else [__after(__d) for __d.outfilename in [((__d.infilename+'.ol.py'))]][0])(lambda __d: (lambda ___: __after(__d))(__print(('Writing to %s'%__d.outfilename)))))(lambda __d: None)) if __d.__name__=='__main__' else __after(__d))(lambda __d: None) for __d.VERBOSE in [(__d.True)]][0] for __d.to_one_line in [(lambda original:[[(lambda __after: __d.original if __d.len(__d.original.splitlines())==1 else __after(__d))(lambda __d: [__d.code(__d.t) for __d.t in [(__d.ast.parse(__d.original))]][0]) for __d.original in [(__d.original.strip())]][0] for __d.original in [(original)]][0])]][0] for __d.code_with_after in [(lambda tree,after:[(lambda __after: '+' if __d.type(__d.tree) is __d.ast.Add else (lambda __after: ' and ' if __d.type(__d.tree) is __d.ast.And else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.Assert else (lambda __after: [[[('[%s for %s in [(%s)]][0]'%(__d.after,__d.targets,__d.value)) for __d.targets in [(','.join(__d.targets))]][0] for __d.value in [(__d.code(__d.tree.value))]][0] for __d.targets in [([__d.code(__d.target) for __d.target in __d.tree.targets])]][0] if __d.type(__d.tree) is __d.ast.Assign else (lambda __after: ('%s.%s'%(__d.code(__d.tree.value),__d.tree.attr)) if __d.type(__d.tree) is __d.ast.Attribute else (lambda __after: [[[('[%s for %s in [%s%s%s]][0]'%(__d.after,__d.target,__d.target,__d.op,__d.value)) for __d.value in [(__d.code(__d.tree.value))]][0] for __d.op in [(__d.code(__d.tree.op))]][0] for __d.target in [(__d.code(__d.tree.target))]][0] if __d.type(__d.tree) is __d.ast.AugAssign else (lambda __after: ('(%s%s%s)'%(__d.code(__d.tree.left),__d.code(__d.tree.op),__d.code(__d.tree.right))) if __d.type(__d.tree) is __d.ast.BinOp else (lambda __after: '&' if __d.type(__d.tree) is __d.ast.BitAnd else (lambda __after: '|' if __d.type(__d.tree) is __d.ast.BitOr else (lambda __after: '^' if __d.type(__d.tree) is __d.ast.BitXor else (lambda __after: ('(%s)'%__d.code(__d.tree.op).join([__d.code(__d.val) for __d.val in __d.tree.values])) if __d.type(__d.tree) is __d.ast.BoolOp else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.Break else (lambda __after: [[[(lambda __after: [__after(__d) for __d.starargs in [([])]][0] if __d.tree.starargs is __d.None else [__after(__d) for __d.starargs in [([('*'+__d.code(__d.tree.starargs))])]][0])(lambda __d: (lambda __after: [__after(__d) for __d.kwargs in [([])]][0] if __d.tree.kwargs is __d.None else [__after(__d) for __d.kwargs in [([('**'+__d.code(__d.tree.kwargs))])]][0])(lambda __d: [[('%s(%s)'%(__d.func,__d.comma_sep_elems)) for __d.comma_sep_elems in [(','.join(__d.elems))]][0] for __d.elems in [((((__d.args+__d.keywords)+__d.starargs)+__d.kwargs))]][0])) for __d.keywords in [([__d.code(__d.kw) for __d.kw in __d.tree.keywords])]][0] for __d.args in [([__d.code(__d.arg) for __d.arg in __d.tree.args])]][0] for __d.func in [(__d.code(__d.tree.func))]][0] if __d.type(__d.tree) is __d.ast.Call else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.ClassDef else (lambda __after: None if __d.type(__d.tree) is __d.ast.Compare else (lambda __after: (('for %s in %s'%(__d.code(__d.tree.target),__d.code(__d.tree.iter)))+''.join([(' if '+__d.code(__d.i)) for __d.i in __d.tree.ifs])) if __d.type(__d.tree) is __d.ast.comprehension else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.Continue else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.Delete else (lambda __after: ('{%s}'%','.join([('%s:%s'%(__d.code(__d.k),__d.code(__d.v))) for (__d.k,__d.v) in __d.zip(__d.tree.keys,__d.tree.values)])) if __d.type(__d.tree) is __d.ast.Dict else (lambda __after: ('{%s}'%' '.join(([((__d.code(__d.tree.key)+':')+__d.code(__d.tree.value))]+[__d.code(__d.gen) for __d.gen in __d.tree.generators]))) if __d.type(__d.tree) is __d.ast.DictComp else (lambda __after: '/' if __d.type(__d.tree) is __d.ast.Div else (lambda __after: '...' if __d.type(__d.tree) is __d.ast.Ellipsis else (lambda __after: '==' if __d.type(__d.tree) is __d.ast.Eq else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.ExceptHandler else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.Exec else (lambda __after: [('(lambda ___: %s)(%s)'%(__d.after,__d.code_to_exec)) for __d.code_to_exec in [(__d.code(__d.tree.value))]][0] if __d.type(__d.tree) is __d.ast.Expr else (lambda __after: __d.code(__d.tree.body) if __d.type(__d.tree) is __d.ast.Expression else (lambda __after: ', '.join([__d.code(__d.dim) for __d.dim in __d.tree.dims]) if __d.type(__d.tree) is __d.ast.ExtSlice else (lambda __after: '//' if __d.type(__d.tree) is __d.ast.FloorDiv else (lambda __after: [[[(lambda __after: __after(__d) if __d.len(__d.tree.orelse) is not 0 else __after(__d))(lambda __d: ('(lambda __d: %s)(reduce((lambda __d, __i:[%s for %s in [__i]][0]),%s,__d))'%(__d.after,__d.body,__d.item,__d.items))) for __d.items in [(__d.code(__d.tree.iter))]][0] for __d.body in [(__d.many_to_one(__d.tree.body,after='__d'))]][0] for __d.item in [(__d.code(__d.tree.target))]][0] if __d.type(__d.tree) is __d.ast.For else (lambda __after: [[[[(lambda __after: (lambda __d: __after(__d))(reduce((lambda __d, __i:[[__d for __d.function_code in [(('%s(%s)'%(__d.code(__d.decorator),__d.function_code)))]][0] for __d.decorator in [__i]][0]),__d.tree.decorator_list,__d)) if __d.len(__d.tree.decorator_list)>0 else __after(__d))(lambda __d: ('[%s for __d.%s in [(%s)]][0]'%(__d.after,__d.tree.name,__d.function_code))) for __d.function_code in [((__d.args+__d.body))]][0] for __d.body in [(('[%s for %s in [(%s)]][0]'%(__d.body,('__d.'+',__d.'.join(__d.arg_names)),','.join(__d.arg_names))))]][0] for __d.body in [(__d.many_to_one(__d.tree.body))]][0] for (__d.args,__d.arg_names) in [(__d.code(__d.tree.args))]][0] if __d.type(__d.tree) is __d.ast.FunctionDef else (lambda __after: [[[[(lambda __after: [[__after(__d) for __d.arg_names in [__d.arg_names+[__d.tree.vararg]]][0] for __d.args in [__d.args+[('*'+__d.tree.vararg)]]][0] if __d.tree.vararg is not __d.None else __after(__d))(lambda __d: (lambda __after: [[__after(__d) for __d.arg_names in [__d.arg_names+[__d.tree.kwarg]]][0] for __d.args in [__d.args+[('**'+__d.tree.kwarg)]]][0] if __d.tree.kwarg is not __d.None else __after(__d))(lambda __d: [(('lambda %s:'%__d.args),__d.arg_names) for __d.args in [(','.join(__d.args))]][0])) for __d.args in [([(__d.a.id if __d.d is __d.None else ((__d.a.id+'=')+__d.code(__d.d))) for (__d.d,__d.a) in __d.args])]][0] for __d.args in [(__d.zip(__d.padded_defaults,__d.tree.args))]][0] for __d.arg_names in [([__d.arg.id for __d.arg in __d.tree.args])]][0] for __d.padded_defaults in [((([__d.None]*(__d.len(__d.tree.args)-__d.len(__d.tree.defaults)))+__d.tree.defaults))]][0] if __d.type(__d.tree) is __d.ast.arguments else (lambda __after: ('%s'%' '.join(([__d.code(__d.tree.elt)]+[__d.code(__d.gen) for __d.gen in __d.tree.generators]))) if __d.type(__d.tree) is __d.ast.GeneratorExp else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.Global else (lambda __after: '>' if __d.type(__d.tree) is __d.ast.Gt else (lambda __after: '>=' if __d.type(__d.tree) is __d.ast.GtE else (lambda __after: [[[('(lambda __after: %s if %s else %s)(lambda __d: %s)'%(__d.body,__d.test,__d.orelse,__d.after)) for __d.orelse in [(__d.many_to_one(__d.tree.orelse,after='__after(__d)'))]][0] for __d.body in [(__d.many_to_one(__d.tree.body,after='__after(__d)'))]][0] for __d.test in [(__d.code(__d.tree.test))]][0] if __d.type(__d.tree) is __d.ast.If else (lambda __after: ('(%s if %s else %s)'%(__d.code(__d.tree.body),__d.code(__d.tree.test),__d.code(__d.tree.orelse))) if __d.type(__d.tree) is __d.ast.IfExp else (lambda __after: (lambda __d: __d.after)(reduce((lambda __d, __i:[(lambda __after: [__after(__d) for __d.alias.asname in [(__d.alias.name)]][0] if __d.alias.asname is __d.None else __after(__d))(lambda __d: [__d for __d.after in [(("[%s for __d.%s in [__import__('%s')]][0]"%(__d.after,__d.alias.asname,__d.alias.name)))]][0]) for __d.alias in [__i]][0]),__d.tree.names,__d)) if __d.type(__d.tree) is __d.ast.Import else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.ImportFrom else (lambda __after: ' in ' if __d.type(__d.tree) is __d.ast.In else (lambda __after: ('%s'%__d.code(__d.tree.value)) if __d.type(__d.tree) is __d.ast.Index else (lambda __after: (__d.INIT_CODE%__d.many_to_one(__d.child_nodes(__d.tree))) if __d.type(__d.tree) is __d.ast.Interactive else (lambda __after: '~' if __d.type(__d.tree) is __d.ast.Invert else (lambda __after: ' is ' if __d.type(__d.tree) is __d.ast.Is else (lambda __after: ' is not ' if __d.type(__d.tree) is __d.ast.IsNot else (lambda __after: '<<' if __d.type(__d.tree) is __d.ast.LShift else (lambda __after: ('%s=%s'%(__d.tree.arg,__d.code(__d.tree.value))) if __d.type(__d.tree) is __d.ast.keyword else (lambda __after: [[[((('('+__d.args)+__d.body)+')') for __d.body in [(('[%s for %s in [(%s)]][0]'%(__d.body,('__d.'+',__d.'.join(__d.arg_names)),','.join(__d.arg_names))))]][0] for __d.body in [(__d.code(__d.tree.body))]][0] for (__d.args,__d.arg_names) in [(__d.code(__d.tree.args))]][0] if __d.type(__d.tree) is __d.ast.Lambda else (lambda __after: [('[%s]'%','.join(__d.elts)) for __d.elts in [([__d.code(__d.elt) for __d.elt in __d.tree.elts])]][0] if __d.type(__d.tree) is __d.ast.List else (lambda __after: ('[%s]'%' '.join(([__d.code(__d.tree.elt)]+[__d.code(__d.gen) for __d.gen in __d.tree.generators]))) if __d.type(__d.tree) is __d.ast.ListComp else (lambda __after: '<' if __d.type(__d.tree) is __d.ast.Lt else (lambda __after: '<=' if __d.type(__d.tree) is __d.ast.LtE else (lambda __after: '%' if __d.type(__d.tree) is __d.ast.Mod else (lambda __after: (__d.INIT_CODE%__d.many_to_one(__d.child_nodes(__d.tree))) if __d.type(__d.tree) is __d.ast.Module else (lambda __after: '*' if __d.type(__d.tree) is __d.ast.Mult else (lambda __after: ('__d.'+__d.tree.id) if __d.type(__d.tree) is __d.ast.Name else (lambda __after: 'not ' if __d.type(__d.tree) is __d.ast.Not else (lambda __after: '!=' if __d.type(__d.tree) is __d.ast.NotEq else (lambda __after: ' not in ' if __d.type(__d.tree) is __d.ast.NotIn else (lambda __after: __d.str(__d.tree.n) if __d.type(__d.tree) is __d.ast.Num else (lambda __after: ' or ' if __d.type(__d.tree) is __d.ast.Or else (lambda __after: __d.after if __d.type(__d.tree) is __d.ast.Pass else (lambda __after: '**' if __d.type(__d.tree) is __d.ast.Pow else (lambda __after: [(lambda __after: ('(lambda ___: %s)(__print(%s))'%(__d.after,__d.to_print)) if __d.after is not 'None' else ('__print(%s)'%__d.to_print))(lambda __d: __after(__d)) for __d.to_print in [(','.join([__d.code(__d.x) for __d.x in __d.tree.values]))]][0] if __d.type(__d.tree) is __d.ast.Print else (lambda __after: '>>' if __d.type(__d.tree) is __d.ast.RShift else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.Raise else (lambda __after: ('repr(%s)'%__d.code(__d.tree.value)) if __d.type(__d.tree) is __d.ast.Repr else (lambda __after: __d.code(__d.tree.value) if __d.type(__d.tree) is __d.ast.Return else (lambda __after: ('set(%s)'%__d.tree.elts) if __d.type(__d.tree) is __d.ast.Set else (lambda __after: ('{%s}'%' '.join(([__d.code(__d.tree.elt)]+[__d.code(__d.gen) for __d.gen in __d.tree.generators]))) if __d.type(__d.tree) is __d.ast.SetComp else (lambda __after: (lambda __after: ('%s:%s'%(__d.code(__d.tree.lower),__d.code(__d.tree.upper))) if __d.tree.step is __d.None else ('%s:%s:%s'%(__d.code(__d.tree.lower),__d.code(__d.tree.upper),__d.code(__d.tree.step))))(lambda __d: __after(__d)) if __d.type(__d.tree) is __d.ast.Slice else (lambda __after: __d.repr(__d.tree.s) if __d.type(__d.tree) is __d.ast.Str else (lambda __after: '-' if __d.type(__d.tree) is __d.ast.Sub else (lambda __after: ('%s[%s]'%(__d.code(__d.tree.value),__d.code(__d.tree.slice))) if __d.type(__d.tree) is __d.ast.Subscript else (lambda __after: (__d.INIT_CODE%__d.many_to_one(__d.child_nodes(__d.tree))) if __d.type(__d.tree) is __d.ast.Suite else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.TryExcept else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.TryFinally else (lambda __after: [(lambda __after: '()' if __d.len(__d.elts) is 0 else (lambda __after: ('(%s,)'%__d.elts[0]) if __d.len(__d.elts) is 1 else ('(%s)'%','.join(__d.elts)))(lambda __d: __after(__d)))(lambda __d: __after(__d)) for __d.elts in [([__d.code(__d.elt) for __d.elt in __d.tree.elts])]][0] if __d.type(__d.tree) is __d.ast.Tuple else (lambda __after: '+' if __d.type(__d.tree) is __d.ast.UAdd else (lambda __after: '-' if __d.type(__d.tree) is __d.ast.USub else (lambda __after: ('(%s%s)'%(__d.code(__d.tree.op),__d.code(__d.tree.operand))) if __d.type(__d.tree) is __d.ast.UnaryOp else (lambda __after: [[[('(__y(lambda __this: (lambda __d: (lambda __after: %s if %s else %s)(lambda __d: %s))))(__d)'%(__d.body,__d.test,__d.orelse,__d.after)) for __d.orelse in [(__d.many_to_one(__d.tree.orelse,after='__after(__d)'))]][0] for __d.body in [(__d.many_to_one(__d.tree.body,after='__this(__d)'))]][0] for __d.test in [(__d.code(__d.tree.test))]][0] if __d.type(__d.tree) is __d.ast.While else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.With else (lambda __after: __after(__d) if __d.type(__d.tree) is __d.ast.Yield else __after(__d))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: __after(__d)))(lambda __d: None) for __d.tree,__d.after in [(tree,after)]][0])]][0] for __d.code in [(lambda tree:[__d.code_with_after(__d.tree,'None') for __d.tree in [(tree)]][0])]][0] for __d.many_to_one in [(lambda trees,after='None':[None for __d.trees,__d.after in [(trees,after)]][0])]][0] for __d.child_nodes in [(lambda tree:[__d.list(__d.ast.iter_child_nodes(__d.tree)) for __d.tree in [(tree)]][0])]][0] for __d.fields in [(lambda tree:[__d.dict(__d.list(__d.ast.iter_fields(__d.tree))) for __d.tree in [(tree)]][0])]][0] for __d.INIT_CODE in [("(lambda __builtin__: (lambda __print, __y, __d: %s)(__builtin__.__dict__['print'],(lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))),type('StateDict',(),__builtin__.__dict__)()))(__import__('__builtin__'))")]][0] for __d.sys in [__import__('sys')]][0] for __d.ast in [__import__('ast')]][0])(__builtin__.__dict__['print'],(lambda f: (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))),type('StateDict',(),__builtin__.__dict__)()))(__import__('__builtin__'))
