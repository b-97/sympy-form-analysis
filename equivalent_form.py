import sympy
from sympy import Expr, Mul, Add
import sys

def mr_equivalent_form(expr):
    try:
        return mr_flatten(expr)
    except:
        print("Unexpected error:", srepr(expr), sys.exc_info()[0])
        return expr
'''
def mr_simplify_negative_muls(expr):
    args = expr.args
    newargs = []
    op = expr.func
    
    if isinstance(expr, Add):
        newargs = list(map(mr_simplify_negative_muls, args))

    if isinstance(expr, Mul):
   '''     

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
        newargs = list(map(mr_flatten, args))
    return op(*newargs,evaluate=False)
