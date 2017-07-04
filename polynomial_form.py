from __future__ import division

from sympy import *
from monomial_form import is_monomial_form

def is_polynomial_form(expr, form="expanded", eval_trig=False):
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

    #If the expression is a monomial or a singleton in the desired form
    if is_monomial_form(expr,form)[0]:
        return (True, "Expression is also a monomial")
    
    #Make sure each term in the polynomial is a monomial
    else:
        for i in range(0, len(expr.args)):
            if not is_monomial_form(expr.args[i]):
                return (False, "Non-monomial detected")

    #Currently, no definition of polynomials allows for monomials that 
    #are combinable by integers, so we can filter those out
    result = integer_proportional_monomials(expr)
    if result[0]:
        return False, result[1]

    if eval_trig:
        result = sin_2_cos_2_simplifiable(expr)
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
    for i in range(0, len(expr.args)):
        #Check to see if any of the other monomials are divisible with integer
        #quotient and no remainder
        if i <= len(expr.args) - 2:
            for j in range(i+1, len(expr.args)):
                if isinstance(expr.args[i], (Number, NumberSymbol)) and \
                    isinstance(expr.args[j], (Number, NumberSymbol)):
                        return (True, "Two monomials are constants")
                if const_divisible(expr.args[i], expr.args[j])[0]:
                    return (True, "Two monomials are divisible by a constant")
    return (False, "No two monomials divisible by a constant")

def sin_2_cos_2_simplifiable(expr):
    '''determines whether the trig identity sin(x)^2 + cos(x)^2 = 1 \
            can be evaluated.
        Will not catch if sin(x)^2 and cos(x)^2 are both multiplied by the 
        same constant.

        Args:
            expr: A standard sympy expression with constants removed
    '''
    #Check to see if any two monomials are actually sin(x)^2 and cos(x)^2
    for i in range(0, len(expr.args)):
        #Check to see if any two monomials are actually sin(x)^2 and cos(x)^2
        if isinstance(expr.args[i],Pow) and i <= len(expr.args) - 2 and \
                expr.args[i].args[1] == 2:
                    if isinstance(expr.args[i].args[0],sin):
                        for j in range(i+1, len(expr.args)):
                            if isinstance(expr.args[j], Pow) and \
                                    isinstance(expr.args[j].args[0],cos) and \
                                    expr.args[j].args[1] == 2 and \
                                    expr.args[j].args[0].args == expr.args[i].args[0].args:
                                        return (True, "cos(x)^2 + sin(x)^2 exists")
                    elif isinstance(expr.args[i].args[0],cos):
                        for j in range(i+1, len(expr.args)):
                            if isinstance(expr.args[j], Pow) and \
                                    isinstance(expr.args[j].args[0],sin) and \
                                    expr.args[j].args[1] == 2 and \
                                    expr.args[j].args[0].args == expr.args[i].args[0].args:
                                        return (True, "cos(x)^2 + sin(x)^2 exists")
    
    return (False, "No such cos(x)^2 + sin(x)^2 exists")


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
        if all(is_monomial_form(i,"expanded")[0] for i in expr.args):
           return (True, "All monomials in polynomial are expanded")
        else:
            return (False, "Monomial in polynomial left partially factored")
    elif isinstance(expr,(Mul,Pow)):
        return is_monomial_form(expr,"expanded")
    elif isinstance(expr, (TrigonometricFunction,InverseTrigonometricFunction)):
        return is_monomial_form(expr.args,"expanded")


def factored_polynomial_form(expr):
    '''determines whether two monomials in a polynomial can be factored.
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

    if len(monomials) != len(set(monomials)):
        return (False, "Two monomials are duplicates")

    return (True, "No combinable monomials")
