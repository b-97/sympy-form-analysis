from __future__ import division

from sympy import *
from monomial_form import *

def is_fully_expanded_polynomial(expr, eval_trig=False):
    if is_monomial_form(expr)[0]:
        return (True, "Expression is also a monomial")

    for i in range(0, len(expr.args)):
        if not is_monomial_form(expr.args[i]):
            return (False, "One or more terms is not a monomial")

    result = const_divisible(expr)
    if result[0]:
        return (False, result[1])

    if isinstance(expr,Add):
        if all(is_monomial_form(i)[0] for i in expr.args):
           return (True, "All monomials in polynomial are expanded")
        else:
            return (False, "Monomial in polynomial left partially factored")
    elif isinstance(expr, Pow):
        if const_to_const(expr)[0]:
            return (False, "Expression is not a singleton, monomial, or polynomial")
        else:
            return is_monomial_form(expr)
    elif isinstance(expr,Mul):
        return is_monomial_form(expr)
    elif isinstance(expr, (TrigonometricFunction,InverseTrigonometricFunction)):
        return is_monomial_form(expr.args)
    
    return (False, "ERROR: Couldn't identify this polynomial!")

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
        return (True, "Expression is also a monomial")
    
    #Make sure each term in the polynomial is a monomial
    for i in range(0, len(expr.args)):
        if not is_factor_factored(expr.args[i]):
            return (False, "One or more terms is not a monomial")

    #Currently, no definition of polynomials allows for monomials that 
    #are combinable by integers, so we can filter those out
    result = const_divisible(expr)
    if result[0]:
        return False, result[1]

    if isinstance(expr, Pow):
        if const_to_const(expr)[0]:
            return (False, "Improper term")
    
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
        return (False, "Two monomials are duplicates")

    return (True, "No combinable monomials")





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
        return (True, "Expression is a singleton raised to any power")
    
    if sum(isinstance(j, Number) for j in expr.args) > 1:
        return (False, "Two factorable integers")

    #If the expression is raised to a power, ensure the power
    #is sane then look at the base
    
    if isinstance(expr, Pow):
        if const_to_const(expr)[0]:
            return (False, "Expression has constant rational base and exponent")
        elif not is_singleton_form(expr.args[1])[1]:
            return (False, "Expression raised to a non-singleton power")
        return is_factor_factored(expr.args[0])
    
    #if it's a Mul instance, take a look at what's inside
    if isinstance(expr,Mul):
        if not all(is_factor_factored(j)[0] for j in expr.args):
            return (False, "Product has factor in non-monomial form")
    
    
    if isinstance(expr,Add):
        #Using the discriminant of a quadratic expression to determine if the
        #expression could be factored further
        #TODO: Refine this definition - This is where the majority of my
        #research will take place
        if degree(expr) > 1 and len(real_roots(expr)) == degree(expr):
            return (False, "Factor in product is not factored")

    if duplicate_bases(expr)[0]:
        return (False, "Duplicate bases found in monomial")

    return (True, "Expression is a factored monomial factor")

def const_divisible(expr):
    '''determines whether the quotient of two expressions is constant divisible
        Const divisible is defined as dividing with constant quotient and 0 remainder
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    OLD CODE BELOW
    '''
    if isinstance(expr,(Add,Mul)):
        for f in expr.free_symbols:
            exprs = rcollect(expr,f)
            if len(expr.args) != len(exprs.args):
                return (True, "Some terms with variables can be combined")
        for i in range(0, len(expr.args)):
            #Check to see if any of the other monomials are divisible with integer
            #quotient and no remainder
            if i <= len(expr.args) - 2:
                for j in range(i+1, len(expr.args)):
                    if isinstance(expr.args[i], (Number, NumberSymbol)) and \
                            isinstance(expr.args[j], (Number, NumberSymbol)):
                                return (True, "Two monomials are constants")
                    q, r = div(expr.args[i], expr.args[j],domain='QQ')
                    if isinstance(q, (Number,NumberSymbol)) and r == 0:
                        return (True, "Some terms can be combined")

    return (False, "No terms can be combined")

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
