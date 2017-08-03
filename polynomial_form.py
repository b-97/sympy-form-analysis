from __future__ import division
from sympy.functions.elementary.trigonometric import TrigonometricFunction
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction
import sympy
from sympy import Add,Mul,rcollect,Number,NumberSymbol,sin,cos,Pow,Integer,Symbol,gcd,div,degree, Derivative, discriminant, primitive, real_roots
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

    '''
                Polynomials that are not squarefree by definition have
                [d/d(symbol)](expr) as a factor. Currently checking for
                squarefree polynomials increases the length of calculations,
                but tests need to be made to check for this.
    result = is_squarefree_polynomial(expr)
    if not result[0]:
        return result
    '''
    
    #Next, we check to see if individual terms in the polynomial are numerically
    #reducible (i.e, 3/3, x/x x^2/x, etc.)
    if isinstance(expr, Add):
        for i in expr.args:
            result = is_numerically_reducible_monomial(i)
            if result[0]:
                return False, result[1]
    else:
        result = is_numerically_reducible_monomial(expr)
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
    #elif domain == 'ZZ':
    #    result = integer_field_reducible(expr)
    #    return not result[0], result[1]
    elif domain == 'QQ':
        result = real_field_reducible(expr)
        return not result[0], result[1]
    else:
        return False, ErrorOutput.strout("ERROR")

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

    if isinstance(expr, Pow):
        return integer_field_reducible(expr.args[0])

    if sum(isinstance(j, (Integer, int)) for j in real_roots(expr)) > 1:
        return True, PolynomialOutput.strout("INTEGER_HIGH_DEGREE")

    return False, PolynomialOutput.strout("INTEGER_FACTORED")

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

    if isinstance(expr, Add):
        result = is_rational_content_free_polynomial(expr) #TO BE DEFINED
        if not result[0]:
            return True, result[1]

    if isinstance(expr, Mul):
        for i in expr.args:
            result = rational_field_reducible(i)
            if result[0]:
                return result

    if isinstance(expr, Pow):
        return rational_field_reducible(expr.args[0])

    if degree(expr) > 2:
        return False, PolynomialOutput.strout("RATIONAL_HIGH_DEGREE")

    expr_discrim = discrimininant(expr)
    if expr_discrim > 2:
        if all(isinstance(num, Rational) for num in expr.coeffs() + [expr_discrim]):
            return True, PolynomialOutput.strout("RATIONAL_HIGH_DEGREE")

    return False, PolynomialOutput.strout("RATIONAL_FACTORED")
    
