from __future__ import division
from sympy.functions.elementary.trigonometric import TrigonometricFunction
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction
import sympy
from sympy import Add,Mul,rcollect,Number,NumberSymbol,sin,cos,Pow,Integer,Symbol,fraction,gcd,div,degree,Derivative
from .monomial_form import *
from .form_utils import *
from .form_output import *

def is_fully_expanded_polynomial(expr, eval_trig=False):
    '''Determines if a proper polynomial is fully expanded.
        A polynomial that is fully expanded is defined as a sum of monomials
            that cannot be expanded further.
        Args:
            expr: A standard sympy expression
        Returns:
            a tuple containing:
                [0] - boolean result of the function
                [1] - string describing the result
    '''
    result = is_monomial_form(expr)
    if is_monomial_form(expr)[0]:
        return True, result[1]
    elif isinstance(expr, (TrigonometricFunction,InverseTrigonometricFunction)):
        return is_fully_expanded_polynomial(expr.args)
    elif not isinstance(expr, (Add)):
        return False, result[1]
    
    result = const_divisible(expr)
    if result[0]:
        return False, result[1]

    if all(is_monomial_form(i)[0] for i in expr.args):
        return True, PolynomialOutput.strout("EXPANDED")
    else:
        return False, PolynomialOutput.strout("NOT_EXPANDED")

    return False, ErrorOutput.strout("ERROR")

def is_fully_factored_polynomial(expr, eval_trig=False, domain='Z'):
    '''Determines if a proper polynomial is fully expanded.
        A polynomial that is fully factored is defined as a sum or product of
            polynomials that cannot be reduced further.
        Args:
            expr: A standard sympy expression
        Returns:
            a tuple containing:
                [0] - boolean result of the function
                [1] - string describing the result
    '''

    #If the expression is a monomial or a singleton in the desired form
    if is_monomial_form(expr)[0]:
        return True, PolynomialOutput.strout("IS_MONOMIAL")

    #Polynomials that are not squarefree by definition have
    #[d/d(symbol)](expr) as a factor, so it may be a good idea to factor
    #those out

    result = is_squarefree_polynomial(expr)
    if not result[0]:
        return result
    

    if not isinstance(expr,Add):
        result = is_numerically_reducible_monomial("expr")
        if result[0]:
            return False, result[1]
    else:
        for i in expr.args:
            result = is_numerically_reducible_monomial(i)
            if result[0]:
                return False, result[1]

    #Make sure each term in the polynomial is a monomial
    for i in expr.args:
        result = is_factor_factored(i)
        if not result[0]:
            return result

    #Currently, no definition of polynomials allows for monomials that
    #have cancellable terms, so we can filter those out
    result = is_numerically_reducible_monomial(expr)
    if result[0]:
        return False, result[1]


    #Currently, no definition of polynomials allows for monomials that
    #are combinable by integers, so we can filter those out
    result = const_divisible(expr)
    if result[0]:
        return False, result[1]
    
    if eval_trig:
        result = sin_2_cos_2_simplifiable(expr)
        if result[0]:
            return False, result[1]
    
    result = duplicate_bases(expr)
    if result[0]:
        return False, result[1]
    return True, PolynomialOutput.strout("FACTORED")

def is_squarefree_polynomial(expr):
    '''Determines if a polynomial is squarefree. If a polynomial is not
        squarefree, a factor can be found by computing gcd(f,f'), and thus
        is not fully factored.
        Args:
            expr: A standard sympy expression
        Returns:
            A tuple containing:
                [0] - boolean result of the function
                [1] - string describing the result
    '''
    for exprsymbol in expr.free_symbols:
        if gcd(expr, Derivative(expr, exprsymbol)) != 1:
            return False, "Polynomial is not squarefree"
    
    return True, "Polynomial is squarefree"

def is_factor_factored(expr):
    '''Determines whether a term in a monomial is in factored form.
        #TODO: Implementation
        Args:
            expr: A Sympy expression, representing a monomial factor
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    result = is_singleton_form(expr)
    if result[0]:
        return True, result[1]


    if sum(isinstance(j, Number) for j in expr.args) > 1:
        return False, PolynomialOutput.strout("NOT_FACTORED")


    #If the expression is raised to a power, ensure the power
    #is sane then look at the base

    if isinstance(expr, Pow):
        return is_singleton_form(expr.args[1])

    #if it's a Mul instance, take a look at what's inside
    if isinstance(expr,Mul):
        result = is_numerically_reducible_monomial(expr)
        if result[0]:
            return False, result[1]
        if not all(is_factor_factored(j)[0] for j in expr.args):
            return False, PolynomialOutput.strout("NOT_FACTORED")
    
    #If the degree is larger than 2 and there are more than 1 terms, it's not factored
    if isinstance(expr,Add):
        if degree(expr) > 2 and len(expr.args) > 1:
            return False, PolynomialOutput.strout("NOT_FACTORED")

        elif degree(expr) > 1 and len(real_roots(expr)) == degree(expr):
            return False, PolynomialOutput.strout("NOT_FACTORED")

    if duplicate_bases(expr)[0]:
        return False, PolynomialOutput.strout("NOT_FACTORED")

    return True, PolynomialOutput.strout("FACTORED")
