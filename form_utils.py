from sympy import *

def const_divisible(expr1, expr2):
    '''determines whether the quotient of two expressions is constant divisible
        Const divisible is defined as dividing with constant quotient and 0 remainder
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    '''
    q, r = div(expr1, expr2,domain='QQ')
    if isinstance(q, (Number,NumberSymbol)) and r == 0:
        return (True, "Monomials could be factored further")
    else:
        return (False, "Monomials cannot be factored further")


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


def integer_proportional_monomials(expr):
    '''Determines if any monomials in a polynomial are integer proportional.
        (ex: Mul(2,Pow(x,5)) : Mul(9,Pow(x,5)) is proportional by 2:9)
        TODO: Potentially delete const_divisible and integrate into here?
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result 
    '''
    for i in range(0, len(expr.args)):
        #Check to see if any of the other monomials are divisible with integer
        #quotient and no remainder
        if i <= len(expr.args) - 2:
            for j in range(i+1, len(expr.args)):
                if isinstance(expr.args[i], (Number, NumberSymbol)) and \
                    isinstance(expr.args[j], (Number, NumberSymbol)):
                        return (True, "Two monomials are constants")
                if const_divisible(expr.args[i], expr.args[j])[0]:
                    return (True, "Two or more monomials can be factored together")

    return (False, "No two monomials divisible by a constant")


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
