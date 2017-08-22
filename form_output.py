from sympy import srepr

#Singleton related return values
class SingletonOutput():
    messages = {
        'IMPROPER_TERM': 'Improper term in singleton',
        'REDUCIBLE': "Singleton can be reduced",
        'INVALID_SUM': "More than one term in singleton",
        'INVALID_PRODUCT': "Invalid product in singleton",
        'VALID_SUM':"Expression is a valid singleton",
        'VALID_PRODUCT':"Expression is a valid singleton",
        'VALID': "Expression is a singleton",
        'VALID_TRIG': "Expression is a trig function",
        'VALID_INVTRIG': "Expression is an inverse trig function",
        'INVALID': "Not a singleton",
        'COMPLEX': "Expression is a complex number",
        'COMPLEX_NO_REAL': "Complex number that has no real part",
        'REAL': "Expression is a real singleton",
        'IMAGINARY': "Expression is the imaginary unit",
        'IMAGINARY_IMPROPER':"Imaginary Number to improper power"
    }

    @staticmethod
    def strout(key):
        return SingletonOutput.messages.get(key, None)

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+SingletonOutput.messages.get(key, None)


class MonomialOutput():
    #Monomial related return values
    messages = {
        'REDUCIBLE':"Monomial is reducible",
        'EXPANDABLE':"One or more monomials could be expanded",
        'PROPER':"Expression is a proper monomial",
        'IMPROPER':"Expression is not a proper monomial",
        'IS_SINGLETON':"Monomial is also a singleton",
        'MULTIPLE_TERMS':"More than 1 term in monomial"
    }

    @staticmethod
    def strout(key):
        return MonomialOutput.messages.get(key, None)

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+MonomialOutput.messages.get(key, None)

class PolynomialOutput():
    #Polynomial related return values
    messages = {
        'IS_MONOMIAL':"Expression is also a monomial",
        'EXPANDED':"Monomials in expression are expanded",
        'FACTORED':"Expression is fully factored!",
        'NOT_FACTORED':"Expression is not fully factored",
        'NOT_MONOMIAL':"One or more terms is not a proper monomial",
        'NOT_EXPANDED':"Expression is not fully expanded",
        'SQUAREFREE':"Expression is squarefree",
        'NOT_SQUAREFREE':"Expression is not squarefree",
        'CONTENTFREE_MONOMIAL':"Expression is a monomial",
        'CONTENTFREE':"Expression is contentfree",
        'NOT_CONTENTFREE':"Expression is not contentfree",
        'COMPlEX_HIGH_DEGREE':"Expression has a degree higher than 1",
        'COMPLEX_FACTORED':"Expression is simplified over the complex field",
        'REAL_HIGH_DEGREE':"Expression has a degree higher than 2",
        'REAL_FACTORABLE_QUAD':"Quadratic can be factored further",
        'REAL_FACTORED': "Expression is factored within the real numbers",
        'INTEGER_REDUCIBLE':"Expression could be factored further in the integers",
        'INTEGER_FACTORED':"Expression is factored within the integers",
        'RATIONAL_REDUCIBLE':"Expression could be factored further in the rationals",
        'RATIONAL_FACTORED':"Expression is factored in the rationals"
        ''
    }

    @staticmethod
    def strout(key):
        return PolynomialOutput.messages.get(key, None)

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+PolynomialOutput.messages.get(key, None)

class UtilOutput():
    #Utility related return values
    messages = {
        'SIMPLIFIABLE_NUMERATOR':"Numerator can be simplified",
        'SIMPLIFIABLE_DENOMINATOR':"Denominator can be simplified",
        'SIMPLIFIABLE_FRACTION':"Terms in fraction can be cancelled",
        'NOT_SIMPLIFIABLE_FRACTION':"No terms can be cancelled in fraction",
        'CONST_TO_CONST':"Expression is a constant raised to a constant",
        'NOT_CONST_TO_CONST':"Expression isn't a constant raised to a constant",
        'ONE_OVER_N':"Expression is raised to 1/n",
        'ONE_TO_N':"Expression is 1 raised to a power",
        'REDUCIBLE':"Expression is numerically reducible",
        'INVERSE_N':"Expression is raised to -1",
        'CONST_DIVISIBLE':"One or more terms can be combined",
        'NOT_CONST_DIVISIBLE':"Terms cannot be combined by constants",
        'TRIG_CAN_SIMPLIFY':"Can be simplified by a trig identity",
        'TRIG_CANT_SIMPLIFY':"Can't be simplified by trig identities"
    }

    @staticmethod
    def strout(key):
        return UtilOutput.messages.get(key, None)

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+UtilOutput.messages.get(key, None)

class NumBaseOutput():
    messages = {
        'SMALLER_BASE_EXISTS':"Base could be made smaller",
        'SMALLEST_BASE':"Smallest bases possible",
        'SIMPLE_BASES':"No bases can be combined",
        'NOT_SIMPLE_BASES':"Bases can be combined",
        'EXP_0': "Redundant exponent of 0 detected",
        'EXP_1': "Redundant exponent of 1 detected",
        'EXP_OK': "Exponents in expression are OK",
        'MULTIPLE_TERMS':"Multiple terms detected",
        'NOT_POW':"Not an expression raised to a power",
        'SINGLETON':"Expression is also a singleton"
    }
    @staticmethod
    def strout(key):
        return NumBaseOutput.messages.get(key, None)

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+NumBaseOutput.messages.get(key, None)

class ErrorOutput:
    #Error related return values
    messages = {
        'ERROR': "If you see this, we goofed. Email us!"
    }

    @staticmethod
    def strout(key):
        return ErrorOutput.messages.get(key, None)

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+ErrorOutput.messages.get(key, None)
