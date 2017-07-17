from .singleton_form import *
from sympy import Pow, Mul
import itertools

def minimised_exp_bases(expr):
    '''Determines whether individual bases in a term can be broken down. \
            Ex: 8^3 = 2^(3*3) = 2^9 = 512, where 2^9 has minimized expression
            bases, and 8^3 does not. minimised_exp_bases requires
            simplified_exp_bases(expr) to be true as a prerequisite.
        Args:
            expr: A standard sympy expression
        Returns:
            A tuple containing:
                [0] - boolean result of the function
                [1] - string describing result of the function
    '''
    result = simplified_expr_bases(expr)
    if not result[0]:
        return False, result[1]

    bases = _exp_collect_bases(expr)

    for i in bases:
        n = 2
        while (n < i):
            if isinstance(log(i,n), (Integer, int)):
                return False, "Base could be made smaller"
    return True, "No base could be made smaller"

def simplified_exp_bases(expr):
    '''Determines whether bases in an expression are simplified.
        Current definition of "simplified": can two bases in the expression
        be combined?
        Args:
            expr: A Standard Sympy expression
        Returns:
            A tuple containing:
                [0] - boolean result of the function
                [1] - String describing result of the function
    '''
    if isinstance(expr, Pow):
        return _exp_0_or_1(expr)
    
    if any(_exp_0_or_1(i)[0] for i in expr.args):
        return False, "Redundant power detected"

    elif not isinstance(expr, Mul):
        return False, "Not a single term of singletons raised to a power"
    
    bases = _exp_collect_bases(expr)

    for i,j in itertools.combinations(bases, 2):
        if isinstance(log(i,j), Integer):
            return False, "Two bases can be combined"
        elif isinstance(log(j,i), Integer):
            return False, "Two bases can be combined"

    return True, "No two bases can be combined"


def _exp_collect_bases(expr):
    '''Collects all of the bases in a function.
        Args:
            expr: A standard sympy expression
        Returns:
            A tuple containing:
                [0] - boolean result of the function
                [1] - string describing the result
    '''
    bases = []
    for i in expr.args:
        if isinstance(i, Pow):
            bases.append(i.args[0])
        elif isinstance(i,Mul):
            bases += _exp_collect_bases(i)
        else:
            bases.append(i)
    return bases



def _exp_0_or_1(expr):
    '''Determines whether a given expression is raised to 0 or 1, which is \
            redundant algebraically.
        Args:
            expr: A standard Sympy expression
        Returns:
            A tuple containing:
                [0] - boolean result of the function
                [1] - string describing the result
    '''
    if not isinstance(expr, Pow):
        return False, "Not an expression raised to a power"

    if expr.args[1] == 0:
        return True, "Expression raised to redundant power of 0"
    elif expr.args[1] == 1:
        return True, "Expression raised to redundant power of 1"

    return False, "Expression raised to a normal power"
