from __future__ import division

from sympy import *
from sympy.functions.elementary.trigonometric import TrigonometricFunction as SymTrigF
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction as SymInvTrigF

def is_singleton_factor_form(expr):
    '''Determines if a product in a singleton is appropriate.
        1. No symbols are allowed in the product.
        2. Product cannot contain two rational numbers.
        3. Product cannot contain any operations other than Mul.
        Args:
            expr: A Mul Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    for i in expr.args:
        if not isinstance(i, (Number, NumberSymbol)):
            return False, "Singletons cannot have symbols in their products"

    if sum(isinstance(j, Number) for j in expr.args) > 1:
        return False, "> 1 instance of rational numbers inside a product"
    
    return True, "Product appropriate for singletons"

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
    #Collect the bases for later comparison
    bases = []
    
    #We don't want symbols or subexpressions like Add
    for i in expr.args:
        if not isinstance(i, (Number, NumberSymbol, Mul)):
            return True, "Singleton can be combined"

        #If there's a product, make sure only one is rational
        if isinstance(i, Mul):
            bases += i.args
            result = is_singleton_factor_form(i)
            if not result[0]:
                return True, result[1]
        else:
            bases.append(i)
    
    #Any two rational numbers can be simplified
    if sum(isinstance(i, Rational) for i in expr.args) > 1:
        return True, "Two instances of rational numbers"

    if len(bases) != len(set(bases)):
        return True, "Two combinable terms in singleton"
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
        return (True, "Expression is a singleton!")
    
    #Case of rational added to irrational
    if isinstance(expr, Add):
        result = singleton_combinable_terms(expr)
        if result[0]:
            return (False, result[1])
        else:
            return (True, result[1])

    #Case of rational multiplied to irrational
    if isinstance(expr, Mul):
        return is_singleton_factor_form(expr)

        
    #Case of trigonometric functions
    #TODO: Analyze what's inside the trigonometric function
    if isinstance(expr, (SymTrigF)):
        return (True, "Expression is a trigonometric function")
    if isinstance(expr, SymInvTrigF):
        return (True, "Expression is an inverse trig function")
    

    #Case of pi^2, pi^pi, pi^x, etc.
    if isinstance(expr,Pow) and isinstance(expr.args[0],NumberSymbol) and \
            isinstance(expr.args[1],(Symbol,Number,NumberSymbol)):
                return (True, "Expression is a singleton")
    #Case of 3^x, 3^pi, etc.
    if isinstance(expr,Pow) and isinstance(expr.args[0],Number) and \
            isinstance(expr.args[1],(Symbol,NumberSymbol)):
                return (True, "Expression is a singleton")
   
    return (False, "Not a singleton")
