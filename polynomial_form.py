from __future__ import division
from sympy.functions.elementary.trigonometric import TrigonometricFunction
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction
import sympy
from sympy import Add,Mul,rcollect,Number,NumberSymbol,sin,cos,Pow,Integer,Symbol,fraction,gcd,div,degree, Derivative, discriminant
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

def is_fully_factored_polynomial(expr, eval_trig=False, domain='RR'):
    '''Determines if a proper polynomial is fully expanded.
        A polynomial that is fully factored is defined as a sum or product of
            polynomials that cannot be reduced further.
        Args:
            expr: A standard sympy expression
            domain: (optional) determination of the field that the polynomial \
                is to be either reducible or irreducible over. Domain \
                specification is determined by two capital leterts to match \
                sympy's style.
                Options:
                    'RR' - Real numbers
                    'CC' - Complex numbers
                    TODO:
                        'QQ' - Rationals
                        'ZZ' - Integers
        Returns:
            a tuple containing:
                [0] - boolean result of the function
                [1] - string describing the result
    '''

    #If the expression is already a  monomial or a singleton in the desired form
    if is_monomial_form(expr)[0]:
        return True, PolynomialOutput.strout("IS_MONOMIAL")

    #Polynomials that are not squarefree by definition have
    #[d/d(symbol)](expr) as a factor, so it may be a good idea to factor
    #those out for speed
    result = is_squarefree_polynomial(expr)
    if not result[0]:
        return result
    

    if isinstance(expr, Add):
        for i in expr.args:
            result = is_numerically_reducible_monomial(i)
            if result[0]:
                return False, result[1]
        result = is_factor_factored(i)
        if not result[0]:
            return result
    else:
        result = is_numerically_reducible_monomial(expr)
        if result[0]:
            return False, result[1]
        for i in expr.args:
            result = is_factor_factored(i)
            if not result[0]:
                return False, result[1]

    #Currently, no definition of polynomials allows for monomials that
    #are combinable by integers, so we can filter those out
    result = const_divisible(expr)
    if result[0]:
        return False, result[1]

    result = duplicate_bases(expr)
    if result[0]:
        return False, result[1]

    if domain == 'RR':
        result = real_field_reducible(expr)
        return not result[0], result[1]
    elif domain == 'CC':
        result = complex_field_reducible(expr)
        return not result[0], result[1]
    else:
        return False, UtilOutput.strout("ERROR")

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
            return False, PolynomialOutput.strout("NOT_SQUAREFREE")
    
    return True, PolynomialOutput.strout("SQUAREFREE")

def is_content_free_polynomial(expr):
    '''Determines if a polynomial is content-free. A polynomial that has
        content is defined to have an integer gcd between all monomials that
        is not equal to 1. Will always return false if there is only one term
        in the expression,
        Args:
            expr: A standard sympy expression
        Returns:
            A tuple containing:
                [0] - boolean result of the function
                [1] - string describing the result
                [2] - integer content of the polynomial
    '''
    if not isinstance(expr, Add):
        return False, PolynomialOutput.strout("CONTENTFREE_MONOMIAL"), 1
    
    result = primitive(expr)

    if primitive(expr)[0] != 1:
        return False, PolynomialOutput.strout("NOT_CONTENTFREE"), primitive(expr)[0]

    return True, PolynomialOutput.strout("CONTENTFREE"), 1


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

    if duplicate_bases(expr)[0]:
        return False, PolynomialOutput.strout("NOT_FACTORED")

    return True, PolynomialOutput.strout("FACTORED")

def complex_field_reducible(expr):
    '''Determines if the polynomial is reducible over the complex field.
    According to the fundamental theorem of algebra, a polynomial is reducible
    if and only if the degree is one. However, for this library, we won't count
    monomials such as x^4, as being reducible.
    Args:
        expr: a standard Sympy expression
    Returns:
        a tuple containing:
            [0] - boolean result of the function
            [1] - string describing the result
    '''
    result = is_monomial_form(expr)
    if result[0]:
        return False, PolynomialOutput.strout("IS_MONOMIAL")
    
    if degree(expr) > 1:
        return True, PolynomialOutput.strout("COMPLEX_HIGH_DEGREE")
    
    return False, PolynomialOutput.strout("COMPLEX_FACTORED")

def real_field_reducible(expr):
    '''Determines if the polynomial is reducible over the real field.
    According to the fundamental theorem of algebra, a polynomial is reducible
    if and only if the following criterion are met:
        1: Degree of polynomial is less than 3.
        2: If degree of polynomial is 2, at least one of the roots are in
            the complex field.
    However, for this library, we won't count monomials, such as x^4, 
        as being reducible.
    Args:
        expr: a standard Sympy expression
    Returns:
        a tuple containing:
            [0] - boolean result of the function
            [1] - string describing the result
    '''
    result = is_monomial_form(expr)
    if result[0]:
        return False, PolynomialOutput.strout("IS_MONOMIAL")

    if degree(expr) > 2:
        return True, PolynomialOutput.strout("REAL_HIGH_DEGREE")

    if degree(expr) == 2 and discriminant(expr) >= 0:
        return True, PolynomialOutput.strout("REAL_FACTORABLE_QUAD")

    return False, PolynomialOutput.strout("REAL_FACTORED")

def integer_field_reducible(expr):
    '''Determines if the polynomial is reducible over the field of integers.
        The current working definition of a polynomial reducible over the \
                integers is one that has more than two integer roots or has \
                content that can be factored.
    However, for this library, we won't count monomials, such as x^4, 
        as being reducible.
    Args:
        expr: a standard Sympy expression
    Returns:
        a tuple containing:
            [0] - boolean result of the function
            [1] - string describing the result
    '''
    
    result = is_monomial_form(expr)
    if result[0]:
        return False, PolynomialOutput.strout("IS_MONOMIAL")

    result = is_content_free_polynomial
    if not result[0]:
        return True, result[1]

    if sum(isinstance(j, (Integer, int)) for j in real_roots(expr)) > 1:
        return True, PolynomialOutput.strout("INTEGER_HIGH_DEGREE")

    return False, PolynomialOutput.strout("INTEGER_FACTORED")
