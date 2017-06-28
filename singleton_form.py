from sympy import *
from sympy.functions.elementary.trigonometric import TrigonometricFunction
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction

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
    A singleton is defined to be either a number or a symbol
    returns:    true if so
                false if not
    Note: internally, 0 + 6 will pass as a singleton, because SymPy will 
        convert 0 + 6 to 6. This is SymPy's fault; if the issue is handled it
        won't be here.
'''
def is_singleton_form(expr):
    if isinstance(expr, (Number, NumberSymbol, Symbol)):
        return (True, "Expression is a number, NumberSymbol, or Symbol")
    
    #Case of rational added to irrational
    if isinstance(expr, Add):
        result = singleton_combinable_terms(expr)
        if result[0]:
            return (False, result[1])
        else:
            return (True, result[1])

    #Case of trigonometric functions
    #TODO: Analyze what's inside the trigonometric function
    if isinstance(expr, (TrigonometricFunction)):
        return (True, "Expression is a trigonometric function")
    if isinstance(expr, InverseTrigonometricFunction):
        return (True, "Expression is an inverse trig function")
    
    return (False, "Not a singleton")
