from sympy import *

#Returns whether expression in question is a real number
#to the power of a real number.
def const_to_const(expr):
    return isinstance(expr, Pow) and \
            isinstance(expr.args[0], Number) and \
            isinstance(expr.args[1], Number)

#returns whether the exponent is a constant or not
def const_expon(expr):
    return isinstance(expr, Pow) and \
        (isinstance(expr.args[1], Number) or \
        isinstance(expr.args[1], NumberSymbol))

#Returns if an expression is a singleton.
def is_singleton(expr):
    if isinstance(expr, Number):
        return True
    elif isinstance(expr, NumberSymbol):
        return True
    elif isinstance(expr, Symbol):
        return True
            
    #First: test to see if it's raised to a power
    #If so, make sure the exponent constant and 
    #ensure the base is in singleton form
    if isinstance(expr, Pow):
        #TODO: Add code to pass bases like (pi + 3)
        if isinstance(expr.args[0], Mul):
            return False
        if const_to_const(expr):
            return False
        elif isinstance(expr.args[0], Add):
            return False
        else:
            return True
    return False 
