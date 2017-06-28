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
    singleton_combinable_terms(expr): determines if two terms in a singleton
        can be combined.
            TODO LIST:
                1. Two rational numbers are combinable (DONE!)
                2. Two identical irrational numbers are combinable (Done!)
                3. Two irrational numbers with combinable terms (pi, sqrt(2), etc)
                    are combinable
    returns:    true if so
                false if not
'''
def singleton_combinable_terms(expr):
    
    #We don't want symbols or subexpressions like Add
    for i in expr.args:
        if not isinstance(i, (Number, NumberSymbol, Mul)):
            return True

        #If there's a product, make sure only one is rational
        if isinstance(i, Mul):
            if sum(isinstance(j, Number) for j in i.args) > 1:
                return True

    #Any two rational numbers can be simplified
    if sum(isinstance(i, Rational) for i in expr.args) > 1:
        return True
   
    #Evaluate each individual term numerically - if duplicates, return true
    return len(expr.args) != len(set(map(N, expr.args)))

'''
    is_singleton(expr) - determines if the expression is a singleton
    A singleton is defined to be either a number or a symbol, optionally raised
    to a power.
    returns:    true if so
                false if not
    Note: internally, 0 + 6 will pass as a singleton, because SymPy will convert 0 + 6 to 6. This is
        SymPy's fault; if the issue is handled it won't be
        here.
'''
def is_singleton(expr):
    
    #If singular number or symbol
    if isinstance(expr, (Number, NumberSymbol, Symbol)):
        return True
    
    #Case of rational added to irrational
    if isinstance(expr, Add):
        return not singleton_combinable_terms(expr)

    #If number or symbol raised to a power
    if isinstance(expr, Pow):
        if isinstance(expr.args[0], Mul):
            return False
        if const_to_const(expr):
            return False
        elif isinstance(expr.args[0], Add):
            return not singleton_combinable_terms(expr)
        else:
            return True
    return False 
