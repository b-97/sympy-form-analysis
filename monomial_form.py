from sympy import *
from singleton_form import *

def const_to_const(expr):
    '''determines if an expression is a rational raised to a constant \
            power other than 1 and 1/n"
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    '''
    if isinstance(expr, Pow) and isinstance(expr.args[0], Number):
        if isinstance(expr.args[1], Pow):
            if expr.args[1].args[1] == -1:
                return (False, "Singleton raised to 1/n")
            elif expr.args[1] == -1:
                return (False, "Singleton raised to -1")
        elif isinstance(expr.args[1], Number):
            return (True, "Singleton is a const to a const")
    
    return (False, "Singleton is not a const to a const")

def is_monomial_factor_form(expr):
    '''Determines whether a term in a monomial is in the appropriate form.
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    if isinstance(expr, Pow):
        if const_to_const(expr)[0]:
            return (False, "Expression has constant rational base and exponent")
        if not is_singleton_form(expr.args[0])[0]:
            return (False, "Expression is not a monomial")
        elif not is_singleton_form(expr.args[1])[1]:
            return (False, "Expression raised to a non-singleton power")
    elif not is_singleton_form(expr)[0]:
        return (False, "Non-singleton monomial factor found")
    return (True, "Monomial is in factor form")

def is_monomial_form(expr):
    '''Determines whether an expression is in proper monomian form.
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
        return (True, "Expression is in singleton form")
    elif isinstance(expr,Pow):
        return is_monomial_factor_form(expr)
    elif isinstance(expr,Add):
        return (False, "Expression has multiple terms")
    if sum(isinstance(j, Number) for j in expr.args) > 1:
        return (False, "No more than 1 number coefficient allowed!")
    if isinstance(expr,Mul):
        if not all(is_monomial_form(j) for j in expr.args):
            return (False, "Non-monomial found in Mul expression")

    result = duplicate_bases(expr)
    if result[0]:
        return (False, "Duplicate base found in monomial")
    else:
        return (True, "Expression is a monomial")

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
    bases = []
    
    #collect the bases - if there's an exponent, just look at the base
    for i in range(0, len(expr.args)):
        if isinstance(expr.args[i], Pow):
            bases.append(expr.args[i].args[0])
        else:
            bases.append(expr.args[i])

    #Set only collects unique bases
    if len(bases) != len(set(bases)):
        return (True, "Bases can be combined")
    else:
        return (False, "No combinable bases found")
