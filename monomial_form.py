from __future__ import division
from sympy import *
from singleton_form import *

#TODO: Remove this function, integrate into polynomial_form
def is_factored_monomial(expr):
    if is_singleton_form(expr)[0]:
        return (True, "Expression is also a singleton")
    
    elif isinstance(expr,Pow):
        return is_monomial_factor_factored_form(expr)
        
    if sum(isinstance(j, Number) for j in expr.args) > 1:
        return (False, "Two factorable integers")
    
    if isinstance(expr,Add):
        return (False, "More than 1 term in expression")

    if isinstance(expr,Mul):
        if not all(is_monomial_factor_factored_form(j)[0] for j in expr.args):
            return (False, "Improper factor in product")

    if duplicate_bases(expr)[0]: 
        return (False, "Duplicate base found in monomial")
    
    return (True, "Expression is a factored monomial")


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
        return is_monomial_factor_expanded_form(expr)
        
    if sum(isinstance(j, Number) for j in expr.args) > 1:
        return (False, "Two factorable integers")
    
    if isinstance(expr,Add):
        return (False, "More than 1 term in expression")

    if isinstance(expr,Mul):
        if not all(is_monomial_factor_expanded_form(j)[0] for j in expr.args):
            return (False, "Improper factor in product")

    if duplicate_bases(expr)[0]: 
        return (False, "Duplicate base found in monomial")
    
    return(True, "Expression is an expanded monomial")


#TODO: COMBINE IS_MONOMIAL_FACTORED_FORM AND IS_MONOMIAL_EXPANDED_FORM

def is_monomial_factor_expanded_form(expr):
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
            return (False, "Expression has a constant rational base and exponent")
        elif not is_singleton_form(expr.args[0])[0]:
            return (False, "Expression is not a monomial")
        elif not is_singleton_form(expr.args[1])[1]:
            return (False, "Expression raised to a non-singleton power")
    elif isinstance(expr, Mul):
        if not all(is_monomial_factor_expanded_form(j)[0] for j in expr.args):
            return (False, "Term in product is not an expanded monomial")
    elif not is_singleton_form(expr)[0]:
        return (False, "Non-singleton monomial factor found")
    return (True, "Monomial is in factor form")


#TODO: Remove, integrate into polynomial form
def is_monomial_factor_factored_form(expr):
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
        return (True, "Expression is a monomial")
    if isinstance(expr, Pow):
        if const_to_const(expr)[0]:
            return (False, "Expression has constant rational base and exponent")
        elif not is_singleton_form(expr.args[1])[1]:
            return (False, "Expression raised to a non-singleton power")
        expr = expr.args[0]
    if isinstance(expr,Mul):
        if not all(is_monomial_factor_factored_form(j)[0] for j in expr.args):
            return (False, "Product has factor in non-monomial form")
    if isinstance(expr,Add):
        #Using the discriminant of a quadratic expression to determine if the
        #expression could be factored
        if degree(expr) > 1 and len(real_roots(expr)) == degree(expr):
            return (False, "Factor in product is not factored")
    return (True, "Expression is a factored monomial factor")

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
