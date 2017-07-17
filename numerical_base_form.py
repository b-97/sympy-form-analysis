from .form_output import NumBaseOutput
from .singleton_form import is_singleton_form

from sympy import Pow, Mul,Number,Integer,log
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
    result = simplified_exp_bases(expr)
    if not result[0]:
        return False, result[1]

    bases = _exp_collect_bases(expr)

    for i in bases:
        if isinstance(i, (int,Number)):
            n = 2
            while (n < i):
                if isinstance(log(i,n), (Integer, int)):
                    return False, NumBaseOutput.strout("SMALLER_BASE_EXISTS")
                n += 1

    return True, NumBaseOutput.strout("SMALLEST_BASE")

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
    elif is_singleton_form(expr):
        return True, NumBaseOutput.strout('SINGLETON')
    elif not isinstance(expr, Mul):
        return False, NumBaseOutput.strout('MULTIPLE_TERMS')
    
    for i in expr.args:
        result = _exp_0_or_1(i)[0]
        if result[0]:
            return False, result[1]
    
    bases = _exp_collect_bases(expr)

    for i,j in itertools.combinations(bases, 2):
        if isinstance(log(i,j), Integer):
            return False, NumBaseOutput.strout('NOT_SIMPLE_BASES')
        elif isinstance(log(j,i), Integer):
            return False, NumBaseOutput.strout('NOT_SIMPLE_BASES')

    return True, NumBaseOutput.strout('SIMPLE_BASES')


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
        return False, NumBaseOutput.strout('NOT_POW')

    if expr.args[1] == 0:
        return True, NumBaseOutput.strout('EXP_0')
    elif expr.args[1] == 1:
        return True, NumBaseOutput.strout('EXP_1')

    return False, NumBaseOutput.strout("EXP_OK")
