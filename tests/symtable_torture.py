# This test is designed to complain about any deviation from the
# traversal order used by symtable.

def only_for_parsing():

    @decorator0(lambda: decorator_arg0)
    @decorator1(lambda: decorator_arg1)
    def function_def(
        function_arg0=lambda: function_default0,
        function_arg1=lambda: function_default1,
        *function_args, **function_kwargs):
        lambda: function_body
        return lambda: return_value

    @class_decorator0(lambda: class_decorator_arg0)
    @class_decorator1(lambda: class_decorator_arg1)
    class class_def(lambda: class_base0, lambda: class_base1):
        lambda: class_body

    del (lambda: del_value0).attr, \
        (lambda: del_value1)[lambda: del_index], \
        (lambda: del_value2)[lambda: del_lower:lambda: del_upper:lambda: del_step], \
        (lambda: del_value3)[lambda: del_index0, lambda: del_index1], \
        ((lambda: del_value4).attr, (lambda: del_value5).attr), \
        [(lambda: del_value6).attr, (lambda: del_value7).attr]

    (lambda: assign_target0).attr, (lambda: assign_target1).attr \
        = (lambda: assign_target2).attr, (lambda: assign_target3).attr \
        = lambda: assign_value

    (lambda: aug_assign_target0).attr += lambda: aug_assign_value0
    (lambda: aug_assign_target1)[lambda: aug_assign_index] += lambda: aug_assign_value1
    (lambda: aug_assign_target2)[lambda: aug_assign_lower2:lambda: slice_upper2] += lambda: aug_assign_value2
    (lambda: aug_assign_target3)[lambda: aug_assign_lower3:lambda: slice_upper3:lambda: slice_upper3] += lambda: aug_assign_value3

    print lambda: print_arg0, lambda: print_arg1,
    print lambda: print_arg2, lambda: print_arg3
    print >>lambda: print_file0, lambda: print_arg4, lambda: print_arg5,
    print >>lambda: print_file1, lambda: print_arg6, lambda: print_arg7

    for (lambda: for_target).attr in lambda: for_iter:
        lambda: for_body
        break
    else:
        lambda: for_orelse

    while lambda: while_test:
        lambda: while_body
        continue
    else:
        lambda: while_orelse

    if lambda: if_test:
        lambda: if_body
    else:
        lambda: if_orelse

    # TODO: with

    raise lambda: raise_type, lambda: raise_inst, lambda: raise_tback

    try:
        lambda: body
    except lambda: handler_type0 as (lambda: handler_name0).attr:
        lambda: handler_body0
    except lambda: handler_type1 as (lambda: handler_name1).attr:
        lambda: handler_body1
    else:
        lambda: orelse_body

    try:
        lambda: body
    finally:
        lambda: finalbody

    assert lambda: assert_test, lambda: assert_msg

    import import_name0, import_name1 as import_asname1
    from import_from_module import import_from_name0, import_from_name1 as import_from_asname1

    exec (lambda: exec_body) in lambda: exec_globals, lambda: exec_locals

    global global_name

    pass

    (lambda: bool_op_left) or (lambda: bool_op_right)
    (lambda: bin_op_left) + (lambda: bin_op_right)
    not (lambda: unary_op_operand)
    lambda lambda_arg0=lambda: lambda_default0, \
        lambda_arg1=lambda: lambda_default1, \
        *lambda_args, **lambda_kwargs: \
        lambda: lambda_body
    (lambda: if_exp_body) if (lambda: if_exp_test) else lambda: if_exp_orelse
    {lambda: dict_key0: lambda: dict_value0, lambda: dict_key1: lambda: dict_value1}
    {lambda: set_elt0, lambda: set_elt1}

    [lambda: list_comp_elt
     for (lambda: list_comp_target0).attr in lambda: list_comp_iter0
     if lambda: list_comp_test0 if lambda: list_comp_test1
     for (lambda: list_comp_target1).attr in lambda: list_comp_iter1
     if lambda: list_comp_test2 if lambda: list_comp_test3]

    {lambda: set_comp_elt
     for (lambda: set_comp_target0).attr in (lambda: set_comp_iter0)
     if lambda: set_comp_test0 if lambda: set_comp_test1
     for (lambda: set_comp_target1).attr in (lambda: set_comp_iter1)
     if lambda: set_comp_test2 if lambda: set_comp_test3}

    {lambda: dict_comp_key: lambda: dict_comp_value
     for (lambda: dict_comp_target0).attr in (lambda: dict_comp_iter0)
     if lambda: dict_comp_test0 if lambda: dict_comp_test1
     for (lambda: dict_comp_target1).attr in (lambda: dict_comp_iter1)
     if lambda: dict_comp_test2 if lambda: dict_comp_test3}

    (lambda: generator_exp_elt
     for (lambda: generator_exp_target0).attr in (lambda: generator_exp_iter0)
     if lambda: generator_exp_test0 if lambda: generator_exp_test1
     for (lambda: generator_exp_target1).attr in (lambda: generator_exp_iter1)
     if lambda: generator_exp_test2 if lambda: generator_exp_test3)

    # TODO: yield

    (lambda: compare_left) < (lambda: compare_middle) < (lambda: compare_right)

    (lambda: lambda_func)(
        lambda: lambda_arg0,
        lambda: lambda_arg1,
        kwarg=lambda: lambda_value,
        *lambda: lambda_args,
        **lambda: lambda_kwargs)

    `lambda: repr_value`
    17
    "string"

    (lambda: attribute_value).attr
    (lambda: slice2_value)[lambda: slice2_lower:lambda: slice2_upper]
    (lambda: slice3_value)[lambda: slice3_lower:lambda: slice3_upper:lambda: slice3_step]
    (lambda: subscript_value)[lambda: subscript_index]
    (lambda: extslice_value)[lambda: extslice_index0, lambda: extslice_index1]

    name
    [lambda: list_elt0, lambda: list_elt1]
    (lambda: tuple_elt0, lambda: tuple_elt1)
