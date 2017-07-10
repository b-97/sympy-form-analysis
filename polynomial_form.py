from __future__ import division

from sympy import *
from monomial_form import *
from form_utils import *
from form_output import *

def is_fully_expanded_polynomial(expr, eval_trig=False):
    if is_monomial_form(expr)[0]:
        return True, FormOutput.POLYNOMIAL_IS_MONOMIAL

    if not isinstance(expr,Add):
        result = is_numerically_reducible_monomial(expr)
        if result[0]:
            return False, result[1]
    else:
        for i in expr.args:
            result = is_numerically_reducible_monomial(i)
            if result[0]:
                return False, result[1]

    result = const_divisible(expr)
    if result[0]:
        return False, result[1]

    if isinstance(expr,Add):
        if all(is_monomial_form(i)[0] for i in expr.args):
           return True, FormOutput.EXPANDED_MONOMIALS
        else:
            return False, FormOutput.NOT_EXPANDED

    elif isinstance(expr, Pow):
        return is_monomial_form(expr)
    elif isinstance(expr,Mul):
        return is_monomial_form(expr)
    elif isinstance(expr, (TrigonometricFunction,InverseTrigonometricFunction)):
        return is_monomial_form(expr.args)

    return False, FormOutput.ERROR

def is_fully_factored_polynomial(expr, eval_trig=False):
    '''Determines if an expression is in proper polynomial form
        A polynomial is defined as a sum of monomials that cannot be factored
            further. There's a lot of work to do here.
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
    if is_monomial_form(expr)[0]:
        return True, FormOutput.POLYNOMIAL_IS_MONOMIAL

    if not isinstance(expr,Add):
        result = is_numerically_reducible_monomial(expr)
        if result[0]:
            return False, result[1]
    else:
        for i in expr.args:
            result = is_numerically_reducible_monomial(i)
            if result[0]:
                return False, result[1]

    #Make sure each term in the polynomial is a monomial
    for i in range(0, len(expr.args)):
        if not is_factor_factored(expr.args[i]):
            return False, FormOutput.NOT_MONOMIAL

    #Currently, no definition of polynomials allows for monomials that
    #are combinable by integers, so we can filter those out
    result = const_divisible(expr)
    if result[0]:
        return False, result[1]

    if isinstance(expr, Pow):
        if const_to_const(expr)[0]:
            return False, FormOutput.NOT_MONOMIAL

    if eval_trig:
        result = sin_2_cos_2_simplifiable(expr)
        if result[0]:
            return False, result[1]

    monomials = []
    for i in range(0, len(expr.args)):
        if isinstance(expr.args[i], Pow):
            monomials.append(expr.args[i].args[0])
        else:
            monomials.append(expr.args[i])
    if len(monomials) != len(set(monomials)):
        return False, FormOutput.NOT_FACTORED_POLYNOMIAL

    return True, FormOutput.FACTORED_POLYNOMIAL

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
    if is_singleton_form(expr)[0]:
        return True, FormOutput.CONST_TO_CONST

    if sum(isinstance(j, Number) for j in expr.args) > 1:
        return False, FormOutput.NOT_FACTORED_POLYNOMIAL


    #If the expression is raised to a power, ensure the power
    #is sane then look at the base

    if isinstance(expr, Pow):
        if const_to_const(expr)[0]:
            return False, FormOutput.CONST_TO_CONST
        elif not is_singleton_form(expr.args[1])[1]:
            return False, FormOutput.NOT_FACTORED_POLYNOMIAL
        return is_factor_factored(expr.args[0])



    #if it's a Mul instance, take a look at what's inside
    if isinstance(expr,Mul):
        if not all(is_factor_factored(j)[0] for j in expr.args):
            return False, FormOutput.NOT_FACTORED_POLYNOMIAL


    if isinstance(expr,Add):
        #Using the discriminant of a quadratic expression to determine if the
        #expression could be factored further
        #TODO: Refine this definition - This is where the majority of my
        #research will take place
        if degree(expr) > 1 and len(real_roots(expr)) == degree(expr):
            return False, FormOutput.NOT_FACTORED_POLYNOMIAL

    if duplicate_bases(expr)[0]:
        return False, FormOutput.NOT_FACTORED_POLYNOMIAL

    return True, FormOutput.FACTORED_POLYNOMIAL
