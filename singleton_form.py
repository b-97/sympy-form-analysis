from sympy import *

'''
    const_to_const(expr): determines if an expression is a
        non-transcendental number to the power of a non-transcendental number
    returns: true if so
             false if not
'''
def const_to_const(expr):
    return isinstance(expr, Pow) and \
            isinstance(expr.args[0], Number) and \
            isinstance(expr.args[1], Number)

'''
    const_expon(expr) - determines if the expression has an
        non-transcendental exponent.
    returns:    true if so
                false if not
'''
def const_expon(expr):
    return isinstance(expr, Pow) and \
        (isinstance(expr.args[1], Number) or \
        isinstance(expr.args[1], NumberSymbol))

'''
    is_singleton(expr) - determines if the expression is a singleton
    A singleton is defined to be either a number or a symbol, optionally raised
    to a power.
    TODO: Allow numbers like (pi + 12) to be included in the definition
'''
def is_singleton(expr):
    
    #If number or symbol
    if isinstance(expr, Number) or \
            isinstance(expr, NumberSymbol) or \
            isinstance(expr, Symbol):
        return True
            
    #If number or symbol raised to a power
    if isinstance(expr, Pow):
        if isinstance(expr.args[0], Mul):
            return False
        if const_to_const(expr):
            return False
        elif isinstance(expr.args[0], Add):
            return False
        else:
            return True
    return False 
