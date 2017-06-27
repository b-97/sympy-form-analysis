from sympy import *
from singleton_form import *

#Returns if an expression is a monomial or not.
def is_monomial(expr):
    if is_singleton(expr):
        return True
    elif not isinstance(expr, Mul):
        return False
    else:
        for i in range(0,len(expr.args)):
            if not is_singleton(expr.args[i]):
                print(srepr(expr))
                return False
    return not duplicate_bases(expr)

#Test to see if any of the factors are dupes
def duplicate_bases(expr):
    bases = []
    
    #collect the bases - if there's an exponent, just look
    #at the base
    for i in range(0, len(expr.args)):
        if isinstance(expr.args[i], Pow):
            bases.append(expr.args[i].args[0])
        else:
            bases.append(expr.args[i])
    
    #check for any dupes
    return len(bases) != len(set(bases))
