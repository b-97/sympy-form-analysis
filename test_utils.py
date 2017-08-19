import sympy
from sympy.functions import re
from .form_utils import is_numerical_equation

from sympy import Poly, Add, N, Number, NumberSymbol,Add,Mul,srepr,Pow

def polynomial_length(expr):
    '''Determines the size of a polynomial using the formula:
        L(P) = sum(coeffs(i)) for i in polynomial coefficients
        Args:
            Expr: A standard sympy expression
        Returns:
            i: an integer corresponding to the polynomial size
    '''
    if is_numerical_equation(expr)[0]:
        return abs(re(N(expr)))
    if isinstance(expr, Mul) and any(isinstance(arg, Add) for arg in expr.args):
        return sum(polynomial_length(arg) for arg in expr.args)
    return sum(abs(re(N(coef))) for coef in Poly(expr).coeffs())
