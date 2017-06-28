from sympy import *

'''
    const_to_const(expr): determines if an expression is a
        non-transcendental number to the power of a non-transcendental number
    returns a tuple with a boolean result and a message describing the result
'''
def const_to_const(expr):
    if isinstance(expr, Pow) and \
            isinstance(expr.args[0], Number) and \
            isinstance(expr.args[1], Number):
                return True, "Singleton is a const to a const"
    else:
        return False, "Singleton is not a const to a const"

'''
    const_expon(expr) - determines if the expression has an
        non-transcendental exponent.
    returns a tuple with a boolean result and a message describing the result
'''
def const_expon(expr):
    if isinstance(expr, Pow) and \
            isinstance(expr.args[1], (Number, NumberSymbol)):
                return True, "Singleton has a constant exponent"
    else:
        return False, "Singleton does not have a constant exponent"


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
            return True, "Singleton can be combined"

        #If there's a product, make sure only one is rational
        if isinstance(i, Mul):
            #No symbols allowed inside a Mul
            for j in i.args:
                if not isinstance(j, Number, NumberSymbol):
                    return True, "Singletons cannot have symbols in their products"
                if const_to_const(j)[0]:
                    return True, "Mul instance inside singleton has a constant to a constant"

            if sum(isinstance(j, Number) for j in i.args) > 1:
                return True, "Two instances of rational numbers inside a product"

    #Any two rational numbers can be simplified
    if sum(isinstance(i, Rational) for i in expr.args) > 1:
        return True, "Two instances of rational numbers"
   
    #Evaluate each individual term numerically - if duplicates, return true
    if len(expr.args) != len(set(map(N, expr.args))):
        return True, "Two combinable terms"
    else:
        return False, "No combinable terms in singleton"

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
def is_singleton_form(expr):
    
    #If singular number or symbol
    if isinstance(expr, (Number, NumberSymbol, Symbol)):
        return (True, "Expression is a Number, NumberSymbol, or Symbol")
    
    #Case of rational added to irrational
    if isinstance(expr, Add):
        result = singleton_combinable_terms(expr)
        if result[0]:
            return (False, result[1])
        else:
            return (True, result[1])

    #If number or symbol raised to a power
    if isinstance(expr, Pow):
        if isinstance(expr.args[0], Mul):
            result = singleton_combinable_terms(expr)
            print("test")
            if result[0]:
                return (False, result[1])
            else:
                return (True, result[1])
        if const_to_const(expr)[0]:
            return False, "Singleton contains a constant to a constant"
        elif isinstance(expr.args[0], Add):
            result = singleton_combinable_terms(expr)
            if result[0]:
                return (False, result[1])
            else:
                return (True, result[1])
        else:
            return (True, "Singleton raised to a power")
    return (False, "Not a singleton")
