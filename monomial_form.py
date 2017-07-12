from __future__ import division
from sympy.functions.elementary.trigonometric import TrigonometricFunction
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction
import sympy
from sympy import Add,Mul,rcollect,Number,NumberSymbol,sin,cos,Pow,Integer,Symbol,fraction,gcd,div
from singleton_form import *
from form_utils import *

def is_monomial_form(expr):
    '''Determines whether an expression is in proper monomial form.
        Monomials are defined as either a singleton or a single product of
        singletons, where singletons are optionally raised to a power.
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    if is_singleton_form(expr)[0]:
        return True, MonomialOutput.strout("IS_SINGLETON")

    if is_numerically_reducible_monomial(expr)[0]:
        return False, MonomialOutput.strout("REDUCIBLE")

    elif isinstance(expr,Pow):
        if const_to_const(expr)[0]:
            return False, UtilOutput.strout("CONST_TO_CONST")
        if is_singleton_form(expr.args[0])[0]:
            if expr.args[1] == 0 or expr.args[1] == 1:
                return False, MonomialOutput.strout("REDUCIBLE")
            if is_singleton_form(expr.args[1])[0]:
                return True, MonomialOutput.strout("PROPER")
            return False, MonomialOutput.strout("IMPROPER")
        return False, MonomialOutput.strout("EXPANDABLE")
    elif sum(isinstance(j, Number) for j in expr.args) > 1:
        return False, MonomialOutput.strout("REDUCIBLE")
    elif isinstance(expr,Add):
        return False, MonomialOutput.strout("MULTIPLE_TERMS")
    elif isinstance(expr,Mul):
        for j in expr.args:
            if expr.args == 0:
                return False, MonomialOutput.strout("REDUCIBLE")
            result = is_monomial_form(j)
            if not result[0]:
                return False, result[1]

    result = duplicate_bases(expr)

    return not result[0], result[1]

#Check to see if any of the bases in a monomial are duplicates
def duplicate_bases(expr):
    '''Returns if any bases in a monomial are duplicates
        Preconditions: monomial is otherwise well-formed.
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    bases = _search_bases(expr)

    #Set only collects unique bases
    if len(bases) != len(set(bases)):
        return True, MonomialOutput.strout("REDUCIBLE")

    return False, MonomialOutput.strout("PROPER")

def _search_bases(expr):
    '''Searches through the bases in an expression.
        Args:
            expr: A standard Sympy expression
        Returns:
            A set with all of the bases in the expression
    '''
    exprbases = []

    for i in range(0, len(expr.args)):
        if isinstance(expr.args[i], Pow):
            exprbases.append(expr.args[i].args[0])
        elif isinstance(expr.args[i],Mul):
            exprbases += _search_bases(expr.args[i])
        else: #Trig/InverseTrig functions, Add for factored exprs
            exprbases.append(expr.args[i])
    return exprbases
