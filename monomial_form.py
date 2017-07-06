from __future__ import division
from sympy import *
from singleton_form import *


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
        return (True, "Expression is also a singleton")
    
    elif isinstance(expr,Pow):
        if const_to_const(expr)[0]:
            return (False, "Expression has a constant rational base and exponent")
        if is_singleton_form(expr.args[0])[0]:
            if is_singleton_form(expr.args[1])[0]:
                return (True, "Expression is a singleton raised to a \
                        singleton power")
            else:
                return (False, "Expression is not raised to a singleton power")
        else:
            return (False, "Expression is not a singleton")
    
    elif sum(isinstance(j, Number) for j in expr.args) > 1:
        return (False, "Two factorable integers")

    elif isinstance(expr,Add):
        return (False, "More than 1 term in expression")
    
    elif isinstance(expr,Mul):
        for j in expr.args:
            result = is_monomial_form(j)
            if not result[0]:
                return (False, result[1])
        #if not all(is_monomial_form(j)[0] for j in expr.args):
        #    return (False, "Improper factor in product")
    
    if duplicate_bases(expr)[0]: 
        return (False, "Duplicate base found in monomial")
    
    return(True, "Expression is an expanded monomial")

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
    bases = search_bases(expr)

    #Set only collects unique bases
    if len(bases) != len(set(bases)):
        return (True, "Bases can be combined")
    else:
        return (False, "No combinable bases found")

def search_bases(expr):
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
            exprbases += search_bases(expr.args[i])
        else: #Trig/InverseTrig functions, Add instances for factored exprs
            exprbases.append(expr.args[i])
    return exprbases


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
            return (True, "Singleton is a constant raised to a constant")
    
    return (False, "Singleton is not a constant raised to a constant")
