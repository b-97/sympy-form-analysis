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
        isinstance(expr.args[1], (Number, NumberSymbol))

'''
    is_singleton(expr) - determines if the expression is a singleton
    A singleton is defined to be either a number or a symbol, optionally raised
    to a power.
    returns:    true if so
                false if not
    TODO: Potentially refine definition of singletons in the case of an irrational added to a rational
    Note: internally, 0 + 6 will pass as a singleton. This is
        SymPy's fault; if the issue is handled it won't be
        here.
'''
def is_singleton(expr):
    
    #If number or symbol
    if isinstance(expr, (Number, NumberSymbol, Symbol)):
        return True
    
    #Case of rational added to irrational
    #TODO: Something more mathematically sound than counting arguments?
    if isinstance(expr, Add):
        for i in expr.args:
            #only numbers and numbersymbols allowed
            if not isinstance(i, (Number, NumberSymbol)):
                return False
        return len(simplify(expr).args) == len(expr.args)

    #If number or symbol raised to a power
    if isinstance(expr, Pow):
        if isinstance(expr.args[0], Mul):
            return False
        if const_to_const(expr):
            return False
        elif isinstance(expr.args[0], Add):
            if not isinstance(i, (Number, NumberSymbol)):    
                return False
            else: #BANDAID BELOW: PLEASE FIX
                return len(simplify(expr.args[0]).args) == expr.args[0].args
        else:
            return True
    return False 
