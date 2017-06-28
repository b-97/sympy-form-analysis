from sympy import *
from sympy.functions.elementary.trigonometric import TrigonometricFunction
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction

def singleton_combinable_terms(expr):
    '''determines if two terms in a singleton can be combined.
        1. Two rational numbers are combinable.
        2. Two identical rational numbers are combinable.
        3. Two irrational numbers with combinable terms (pi, sqrt(2),etc)
            are combinable
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    '''
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
    if isinstance(expr, Mul):
        for i in expr.args:
            if not isinstance(i, (Number, NumberSymbol)):
                return True, "Singletons cannot have symbols or operations in their products."
        if sum(isinstance(j, Number) for j in expr.args) > 1:
            return True, "Two instances of rational numbers inside a product"

    #Any two rational numbers can be simplified
    if sum(isinstance(i, Rational) for i in expr.args) > 1:
        return True, "Two instances of rational numbers"
   
    #Evaluate each individual term numerically - if duplicates, return true
    if len(expr.args) != len(set(map(N, expr.args))):
        return True, "Two combinable terms"
    else:
        return False, "No combinable terms in singleton"

def is_singleton_form(expr):
    '''determines if the expression is a singleton.
        Note: internally, 0 + 6 will pass as a singleton, because SymPy will
            convert 0 + 6 to 6. This is Sympy's fault; if the issue is handled
            it won't be here.
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    '''
    if isinstance(expr, (Number, NumberSymbol, Symbol)):
        return (True, "Expression is a number, NumberSymbol, or Symbol")
    
    #Case of rational added to irrational
    if isinstance(expr, (Add, Mul)):
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
