import sympy
import itertools

from sympy import Add,Mul,rcollect,Number,NumberSymbol,sin,cos,Pow,Integer,Symbol,fraction,gcd,div,Rational
from sympy.functions.elementary.trigonometric import TrigonometricFunction as SymTrigF
from sympy.functions.elementary.trigonometric import InverseTrigonometricFunction as SymInvTrigF
from .form_output import *

def const_divisible(expr):
    '''determines whether the quotient of two expressions is constant divisible
        Const divisible is defined as dividing with constant quotient and 0 remainder
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    if isinstance(expr,(Add,Mul)):
        for syms in expr.free_symbols:
            exprs = rcollect(expr,syms)
            if len(expr.args) != len(exprs.args):
                return True, UtilOutput.strout("CONST_DIVISIBLE")
        
        
        #Check to see if any of the other monomials are divisible with integer
        #quotient and no remainder
        for i,j in itertools.combinations(expr.args,2):
            if is_numerical_equation(i)[0] and is_numerical_equation(j)[0]:
                return True, UtilOutput.strout("CONST_DIVISIBLE")
            q,r = div(i,j,domain='QQ')
            if isinstance(q, (Number, NumberSymbol)) and r == 0:
                return True, UtilOutput.strout("CONST_DIVISIBLE")

    return False, UtilOutput.strout("NOT_CONST_DIVISIBLE")

def sin_2_cos_2_simplifiable(expr):
    '''determines whether the trig identity sin(x)^2 + cos(x)^2 = 1 \
            can be evaluated.
        Will not catch if sin(x)^2 and cos(x)^2 are both multiplied by the
        same constant.

        Args:
            expr: A standard sympy expression with constants removed
    '''
    #Check to see if any two monomials are actually sin(x)^2 and cos(x)^2
    for i,j in itertools.permutations(expr.args):
        if isinstance(i, Pow) and isinstance(j, Pow) and \
                isinstance(i.args[0], sin) and isinstance(j.args[0], cos) and \
                i.args[1] == 2 and j.args[1] == 2 and \
                expand(i.args[0].args - j.args[0].args) == 0:
                    return True, UtilOutput.strout("TRIG_CAN_SIMPLIFY")

    return False, UtilOutput.strout("TRIG_CANT_SIMPLIFY")

def is_numerical_equation(expr):
    '''Determines if an expresion is a purely numerical equation (contains \
            absolutely no symbols.'
        Particularly useful for preventing an execution of div(N,M), where N \
                and M are constants and Sympy will crash.
        Args:
            expr: A standard sympy expression
        Returns:
            A tuple containing:
                [0]: boolean containing the result
                [1]: string describing the result
    '''
    if isinstance(expr, (int,long,float,complex)):
        return True, "Expression is a basic Python number type"
    elif len(expr.free_symbols) == 0:
        return True, "Expression is a numerical expression"
    
    return False, "Expression is not a purely numerical equation"

def const_to_const(expr):
    '''determines if an expression is a rational raised to a constant \
            power other than -1 and 1/n, or an expression is an equivalent of n/1.
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0]: bool containing the result
                [1]: string describing the result
    '''
    if isinstance(expr, Pow) and isinstance(expr.args[0], Number):
        if expr.args[0] == 1:
            return True, UtilOutput.strout("ONE_TO_N")
        if isinstance(expr.args[1], Pow):
            if expr.args[1].args[1] == -1:
                return False, UtilOutput.strout("ONE_OVER_N")
        elif expr.args[1] == -1:
            return False, UtilOutput.strout("INVERSE_N")
        elif isinstance(expr.args[1], Number):
            return True, UtilOutput.strout("CONST_TO_CONST")

    return False, UtilOutput.strout("CONST_TO_CONST")


def is_numerically_reducible_monomial(expr):
    '''Determines if terms in a monomial could be trivially cancelled out.
        Trivially cancelled out is defined as cancellable without applying any
        factorization or expansion.
        Args:
            expr: A standard sympy expression
        Returns:
            A tuple containing:
                [0] - boolean result of the function
                [1] - string describing the result
    '''
    if isinstance(expr, (Pow,Mul)):
	#First, check to see if it's in form -1*(expr)
        if isinstance(expr, Mul):
            if isinstance(expr.args[0], Integer) and expr.args[0] == -1 and \
                    isinstance(expr.args[1], Mul):
                        expr = expr.args[1]
            #Or if it's in the form (expr)*-1
            elif isinstance(expr.args[1], Integer) and expr.args[1] == -1 and \
                    isinstance(expr.args[0], Mul):
                        expr = expr.args[0]
        
        #Check if the numerator is simplifiable
        if sum(isinstance(j,(Integer,int,float)) for j in fraction(expr)[0].args) > 1:
            return True, UtilOutput.strout("SIMPLIFIABLE_NUMERATOR")

        #Check for simplifiable denominator
        if sum(isinstance(j,(Integer,int,float)) for j in fraction(expr)[1].args) > 1:
            return True, UtilOutput.strout("SIMPLIFIABLE_DENOMINATOR")

        #Finally, collect the numerator and denominator and check if they can be reduced
        if gcd(fraction(expr)[0],fraction(expr)[1]) != 1:
            return True, UtilOutput.strout("SIMPLIFIABLE_FRACTION")

    return False, UtilOutput.strout("NOT_SIMPLIFIABLE_FRACTION")
