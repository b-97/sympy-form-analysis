from sympy import *
from singleton_form import *

'''
    is_monomial_form(expr): returns if an expression is a monomial or not.
    monomials are defined as either a singleton or a single product of singletons
    returns:
        true if the expression is a well-formed monomial
        false otherwise.
'''
def is_monomial_form(expr):
    if is_singleton_form(expr)[0]:
        return (True, "Expression is in singleton form")
    elif not isinstance(expr, Mul):
        return False, "Expression is neither a singleton nor a product of singletons"
    else:
        for i in range(0,len(expr.args)):
            if not is_singleton_form(expr.args[i])[0]:
                return False, "Term found is not a singleton"
    result = duplicate_bases(expr)
    if result[0]:
        return False, "Duplicate base found in monomial"
    else:
        return True, "Expression is a monomial"

'''
    duplicate_bases(expr): returns if any bases in a monomial are duplicates
    Preconditions: monomial is otherwise well-formed
    returns:
        true if there are duplicate bases in the monomial
        false otherwise
'''
#Check to see if any of the bases in a monomial are duplicates
def duplicate_bases(expr):
    bases = []
    
    #collect the bases - if there's an exponent, just look at the base
    for i in range(0, len(expr.args)):
        if isinstance(expr.args[i], Pow):
            bases.append(expr.args[i].args[0])
        else:
            bases.append(expr.args[i])

    #Set only collects unique bases
    if len(bases) != len(set(bases)):
        return True, "Bases can be combined"
    else:
        return False, "No combinable bases found"
