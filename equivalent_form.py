import sympy
from sympy import Expr, Mul, Add
import sys

def mr_equivalent_form(expr):
    '''Larger method to apply equivalent functions to Sympy expressions.
        Current methods that apply is only one: mr_flatten. Plans exist to \
                include more, including negative coefficients for muls, etc.
        Args:
            expr: A standard sympy expression
            associatives: a tuple of operations known to be associative for \
                    the field containing the expression (OPTIONal
        Returns:
            A standard sympy expression, algebraically equivalent to the \
                    supplied expression
    '''
    try:
        return mr_flatten(expr)
    except:
        print("Unexpected error:", srepr(expr), sys.exc_info()[0])
        return expr

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
