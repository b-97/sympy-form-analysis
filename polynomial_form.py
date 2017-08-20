from __future__ import division
from sympy.functions.elementary.trigonometric import TrigonometricFunction
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction
import sympy
from sympy import Add,Mul,rcollect,Number,NumberSymbol,sin,cos,Pow,Integer,Symbol,gcd,div,degree, Derivative, discriminant, primitive, real_roots, sieve
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
    elif not isinstance(expr, (Add)):
        return False, result[1]

    result = const_divisible(expr)
    if result[0]:
        return False, result[1]

    if all(is_monomial_form(i)[0] for i in expr.args):
        return True, PolynomialOutput.strout("EXPANDED")

    return False, PolynomialOutput.strout("NOT_EXPANDED")

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

    #Next, we check to see if individual terms in the polynomial are numerically
    #reducible (i.e, 3/3, x/x x^2/x, etc.)
    for i in mr_polynomial_terms(expr):
        result = is_numerically_reducible_monomial(i)
        if result[0]:
            return False, result[1]

    #Currently, no definition of polynomials allows for monomials that
    #are combinable by integers or by bases, so we can filter those out
    result = const_divisible(expr)
    if result[0]:
        return False, result[1]

    result = duplicate_bases(expr)
    if result[0]:
        return False, result[1]

    #Finally, we analyze the reducibility of the polynomial according to the
    #domain the user specified.
    if domain == 'RR':
        result = real_field_reducible(expr)
        return not result[0], result[1]
    elif domain == 'CC':
        result = complex_field_reducible(expr)
        return not result[0], result[1]
    elif domain == 'ZZ':
        result = integer_field_reducible(expr)
        return not result[0], result[1]
    elif domain == 'QQ':
        result = rational_field_reducible(expr)
        return not result[0], result[1]
    else:
        return False, ErrorOutput.strout("ERROR")

def is_integer_content_free_polynomial(expr):
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
        return True, PolynomialOutput.strout("CONTENTFREE_MONOMIAL"), 1

    result = primitive(expr)

    if primitive(expr)[0] != 1:
        return False, PolynomialOutput.strout("NOT_CONTENTFREE"), primitive(expr)[0]

    return True, PolynomialOutput.strout("CONTENTFREE"), 1

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

    if isinstance(expr, Mul):
        for i in expr.args:
            result = complex_field_reducible(i)
            if result[0]:
                return result
        return False, PolynomialOutput.strout("COMPLEX_FACTORED")

    if isinstance(expr, Pow):
        return complex_field_reducible(expr.args[0])

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

    if isinstance(expr, Mul):
        for i in expr.args:
            result = real_field_reducible(i)
            if result[0]:
                return result
        return False, PolynomialOutput.strout("REAL_FACTORED")

    if isinstance(expr, Pow):
        return real_field_reducible(expr.args[0])

    if degree(expr) > 2:
        return True, PolynomialOutput.strout("REAL_HIGH_DEGREE")

    if degree(expr) == 2 and discriminant(expr) >= 0:
        return True, PolynomialOutput.strout("REAL_FACTORABLE_QUAD")

    return False, PolynomialOutput.strout("REAL_FACTORED")

def integer_field_reducible(expr):
    '''Determines if the polynomial is reducible over the field of integers.
        A polynomial reducible ver the integers is one that has more than two \
                integer roots or has integer content that can be factored.
    However, for this library, we wholly exclude monomials, such as x^4,
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

    if isinstance(expr, Add):
        result = is_integer_content_free_polynomial(expr)
        if not result[0]:
            return True, result[1]

    if isinstance(expr, Mul):
        for i in expr.args:
            result = integer_field_reducible(i)
            if result[0]:
                return result

    expr_poly = Poly(expr, domain=ZZ)
    result = expr_poly.is_irreducible

    if result:
        return False, "Expression is fully factored in the integers"
    return True, "Expression is fully factored in the integers"

def rational_field_reducible(expr):
    '''Determines if the polynomial is reducible over the field of integers.
        A polynomial reducible over the rationals is one that has more than \
                two rational roots or has rational content that can be factored.
    However, for this library, we will wholly exclude monomials, such as x^4,
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

    if isinstance(expr, Mul):
        for i in expr.args:
            result = rational_field_reducible(i)
            if result[0]:
                return result

    if isinstance(expr, Pow):
        return rational_field_reducible(expr.args[0])

    expr_poly = Poly(expr, domain=QQ)
    result = expr_poly.is_irreducible

    if result:
        return False, "Expression is fully factored in the rationals"

    return True, "Expression can be factored further in the rationals"
