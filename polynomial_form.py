from __future__ import division
from sympy import *
from monomial_form import *

def is_polynomial_form(expr):
    '''Determines if an expression is in proper polynomial form
        A polynomial is defined as a sum of monomials that cannot be factored
            further.
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    '''

    #If the expression is a monomial or a singleton
    if is_monomial_form(expr)[0]:
        return (True, "Expression is also a monomial")
    
    #Make sure each term in the polynomial is a monomial
    else:
        for i in range(0, len(expr.args)):
            if not is_monomial_form(expr.args[i]):
                return (False, "Non-monomial detected")
    result = duplicate_monomials(expr)

    if result[0]:
        return (False, result[1])
    else:
        return (True, "Proper Polynomial")

def duplicate_monomials(expr):
    '''Determines if any monomials in a polynomial are factorable
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    '''
    monomials = []
    
    #collect the bases 
    #if there's an exponent, just look at the base
    for i in range(0, len(expr.args)):
        if isinstance(expr.args[i], Pow):
            monomials.append(expr.args[i].args[0])
        else:
            monomials.append(expr.args[i])
        #Check to see if any of the other monomials
        #are divisible with integer quotient and 0
        #remainder
        if i <= len(expr.args) - 2:
            for j in range(i+1, len(expr.args)):
                expr1 = expr.args[i]
                expr2 = expr.args[j]
                expr3 = Add(expr1, expr2, evaluate=False)
                
                #WARNING: THIS IS A BANDAID
                #Merely looks at two expressions and see if Sympy can
                #"simplify" it further
                #Algorithm needs to be developed to replace this block
                #of code
                if isinstance(expr1, (Number, NumberSymbol)) and \
                        isinstance(expr2, (Number,NumberSymbol)):
                            if len(simplify(expr3).args) != \
                                    len(Add(expr3).args):
                                    return (True, "Bandaid applied - Sympy managed to simplify this further")
                                
                if const_divisible(expr.args[i], expr.args[j]):
                    return (True, "Two monomials are divisible by a constant")

    #Check for any duplicates 
    if len(monomials != len(set(monomials))):
        return (True, "Two monomials are duplicates")
    else:
        return (False, "No combinable monomials")

def const_divisible(expr1, expr2):
    '''determines whether the quotient of two expressions is constant divisible
        Const divisible is defined as dividing with constant quotient and 0 remainder
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    '''
    q, r = div(expr1, expr2,domain='QQ')
    if isinstance(q, (Number,NumberSymbol)) and r == 0:
        return (True, "Expressions are divisible by a constant")
    else:
        return (False, "Expressions are not divisible by a constant")
