from __future__ import division
from sympy import *
from monomial_form import *

def is_polynomial_form(expr, form="expanded"):
    '''Determines if an expression is in proper polynomial form
        A polynomial is defined as a sum of monomials that cannot be factored
            further.
        Args:
            expr: A standard Sympy expression
            form: string denoting the desired form
                "factored" - factored form, as succinct as possible
                "expanded" - expanded form
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

    #Currently, no definition of polynomials allows
    #for monomials that are combinable by integers, so we filter those out
    
    result = integer_proportional_monomials(expr)
    if result[0]:
        return False, result[1]

    #Further checks are dependent on user preference
    if form == "factored":
        return factored_polynomial_form(expr)
    elif form == "expanded":
        return expanded_polynomial_form(expr)

def integer_proportional_monomials(expr):
    '''Determines if any monomials in a polynomial are integer proportional.
        (ex: Mul(2,Pow(x,5)) : Mul(9,Pow(x,5)) is proportional by 2:9)
        TODO: Potentially delete const_divisible and integrate into here?
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    '''
    #collect the bases (if there's an exponent, just look at the base)
    for i in range(0, len(expr.args)):
        #Check to see if any of the other monomials are divisible with integer
        #quotient and no remainder
        if i <= len(expr.args) - 2:
            for j in range(i+1, len(expr.args)):
                if const_divisible(expr.args[i], expr.args[j])[0]:
                    print(srepr(expr.args[i]),srepr(expr.args[j]))
                    return (True, "Two monomials are divisible by a constant")
    return (False, "No two monomials divisible by a constant")

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

def expanded_polynomial_form(expr):
    '''determines whether individual monomials in a polynomial can be expanded.
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    '''
    if isinstance(expr,Add):
        if all(expanded_monomial(i)[0] for i in expr.args):
           return (True, "All monomials in polynomial are expanded")
        else:
            return (False, "Monomial in polynomial left partially factored")
    elif isinstance(expr,(Mul,Pow)):
        return expanded_monomial(expr)
    elif isinstance(expr, (TrigonometricFunction,InverseTrigonometricFunction)):
        return expanded_monomial(expr.args)

def expanded_monomial(expr):
    '''determines whether factors in a monomial can be expanded
        For now, just looks at whether there's instances of (Add)
    '''
    if is_singleton_form(expr):
        return (True, ("Expression is a singleton and could not be"
                        "further combined"))
    elif isinstance(expr, Add):
        return (False, "Monomial could be further expanded")
    elif isinstance(expr, Mul):
        if not all(expanded_monomial(i)[0] for i in expr.args):
            return (False, "Factor in monomial could be expanded")
        if not len(expr.args) != len(set(expr.args)):
            return (False, "Duplicate factors in monomial")
    elif isinstance(expr, Pow):
        if not expanded_monomial(expr.args[0])[0]:
            return (False, "Base in monomial could be expanded")
        if not expanded_monomial(expr.args[1])[0]:
            return (False, "Exponent in monomial could be expanded")
    elif isinstance(expr, (TrigonometricFunction,InverseTrigonometricFunction)):
        return expanded_monomial(expr.args)
    return (True, "Monomial cannot be further expanded")

def factored_polynomial_form(expr):
    '''determines whether two monomials in a polynomial can be factored.
        the definition of 'factored' is tenuous and needs to be refined as
        research continues throughout the summer term.
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    monomials = []
    for i in range(0, len(expr.args)):
        if isinstance(expr.args[i], Pow):
            monomials.append(expr.args[i].args[0])
        else:
            monomials.append(expr.args[i])

    if len(monomials != len(set(monomials))):
        return (True, "Two monomials are duplicates")
    else:
        return (False, "No combinable monomials") 
