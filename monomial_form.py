from sympy import *
from singleton_form import *



'''
    const_to_const(expr): determines if an expression is a
    non-transcendental number to the power of a non-transcendental number
    returns a tuple with a boolean result and a message describing the result
'''
def const_to_const(expr):
    if isinstance(expr, Pow) and \
            isinstance(expr.args[0], Number) and \
            isinstance(expr.args[1], Number):
                return (True, "Singleton is a const to a const")
    else:
        return (False, "Singleton is not a const to a const")


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
    elif isinstance(expr,Pow):
        if const_to_const(expr)[0]:
            return (False, "Expression has constant rational base and exponent")
        if not is_singleton_form(expr.args[0])[0]:
            return (False, "Expression is not a monomial")
        elif not is_singleton_form(expr.args[1])[1]:
            return (False, "Expression raised to a non-singleton power")
    elif isinstance(expr,Add):
        return (False, "Expression has multiple terms")
    else:
        if sum(isinstance(j, Number) for j in expr.args) > 1:
            return (False, "No more than 1 number coefficient allowed!")
        for single in expr.args:
            if isinstance(single, Pow):
                if const_to_const(single)[0]:
                    return (False, "Term found with constant rational base and exponent")
                elif not is_singleton_form(single.args[0])[0]:
                    return (False, "Term found with non-singleton base")
                elif not is_singleton_form(single.args[1])[1]:
                    return (False, "Term raised to non-singleton power")
            elif not is_singleton_form(single)[0]:
                return (False, "Term found is not a singleton")

    result = duplicate_bases(expr)
    if result[0]:
        return (False, "Duplicate base found in monomial")
    else:
        return (True, "Expression is a monomial")

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
        return (True, "Bases can be combined")
    else:
        return (False, "No combinable bases found")
