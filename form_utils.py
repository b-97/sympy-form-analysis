from sympy import *
from sympy.functions.elementary.trigonometric import TrigonometricFunction as SymTrigF
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction as SymInvTrigF
from form_output import *

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
                return True, FormOutput.CONST_DIVISIBLE
        for i in range(0, len(expr.args)):
            #Check to see if any of the other monomials are divisible with integer
            #quotient and no remainder
            if i <= len(expr.args) - 2:
                for j in range(i+1, len(expr.args)):
                    if isinstance(expr.args[i], (Number, NumberSymbol)) and \
                            isinstance(expr.args[j], (Number, NumberSymbol)):
                                return True, FormOutput.CONST_DIVISIBLE
                    q, r = div(expr.args[i], expr.args[j],domain='QQ')
                    if isinstance(q, (Number,NumberSymbol)) and r == 0:
                        return True, FormOutput.CONST_DIVISIBLE

    return False, FormOutput.NOT_CONST_DIVISIBLE

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
                                        return True, FormOutput.TRIG_CAN_SIMPLIFY
                    elif isinstance(expr.args[i].args[0],cos):
                        for j in range(i+1, len(expr.args)):
                            if isinstance(expr.args[j], Pow) and \
                                    isinstance(expr.args[j].args[0],sin) and \
                                    expr.args[j].args[1] == 2 and \
                                    expr.args[j].args[0].args == expr.args[i].args[0].args:
                                        return True, FormOutput.TRIG_CAN_SIMPLIFY

    return False, FormOutput.TRIG_CANT_SIMPLIFY

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
                return False, FormOutput.ONE_OVER_N
        elif expr.args[1] == -1:
            return False, FormOutput.INVERSE_N
        elif isinstance(expr.args[1], Number):
            return True, FormOutput.CONST_TO_CONST

    return False, FormOutput.NOT_CONST_TO_CONST


def is_numerically_reducible_monomial(expr):
    #First, rule out the case that it's 1/(const * const)
    if isinstance(expr, Pow):
        if sum(isinstance(j,(Integer,int,float)) for j in expr.args[0].args) > 1:
            return True, FormOutput.SIMPLIFIABLE_DENOMINATOR

    if isinstance(expr, Mul):
	#First, check to see if it's in form -1*(expr)
        if isinstance(expr.args[0], Integer) and expr.args[0] == -1 and \
                isinstance(expr.args[1], Mul):
	    expr = expr.args[1]

        #Then, check to see if there are two integers in the numerator
        if sum(isinstance(j,(Integer,int,float)) for j in expr.args) > 1:
            return True, FormOutput.SIMPLIFIABLE_NUMERATOR

        #Then, check through any denominators that exist:
        for i in expr.args:
            if isinstance(i,Pow):
                if sum(isinstance(j,(Integer,int,float)) for j in expr.args) > 1:
                    return True, FormOutput.SIMPLIFIABLE_DENOMINATOR

        #Finally, collect the numerator and denominator and check if they can be reduced
        q = fraction(expr)[0]
        r = fraction(expr)[1]
        if gcd(q,r) != 1:
            return True, FormOutput.SIMPLIFIABLE_FRACTION

    return False, FormOutput.NOT_SIMPLIFIABLE_FRACTION
