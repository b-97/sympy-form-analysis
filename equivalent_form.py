import sympy
from sympy import *
from sympy.core.operations import AssocOp

def mr_equivalent_form(expr):
    return mr_flatten(expr)

def mr_flatten(expr, associatives=(Mul,Add)):
    '''Walks through a sympy function and applies associative operations.
        Associative operations can be specified explicitly by providing \
                a tuple of associative expressions.
        Args:
            expr: A standard sympy expression
            associatives: A tuple of operations (OPTIONAL)
        Returns:
            A standard sympy expression, but flattened
    '''
    args = expr.args
    newargs = []
    op = expr.func
    if len(args) == 0:
        return expr
    if op in associatives:
        for i in expr.args:
            j = mr_flatten(i)
            if j.func == op:
                newargs += j.args
            else:
                newargs += [j]
    else:
        for i in expr.args:
            newargs += [mr_flatten(i)]
    return op(*newargs,evaluate=False)
