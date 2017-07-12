from sympy import srepr

#Singleton related return values
class SingletonOutput():
    messages = {
        'IMPROPER_SINGLETON_TERM': 'Improper term in singleton',
        'REDUCIBLE_SINGLETON': "Singleton can be reduced",
        'INVALID_SINGLETON_SUM:': "More than one term in singleton",
        'INVALID_SINGLETON_PRODUCT': "Invalid product in singleton",
        'VALID_SINGLETON': "Valid summation in singleton",
        'VALID_SINGLETON_TRIG': "Expression is a trig function",
        'VALID_SINGLETON_INVTRIG': "Expression is an inverse trig function",
        'INVALID_SINGLETON': "Not a singleton"
    }

    @staticmethod
    def strout(key):
        return SingletonOutput.messages.get(key, "No message exists for this type")

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+SingletonOutput.messages.get(key, "No message exists for this type")


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
        return MonomialOutput.messages.get(key, "No message exists for this type")

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+MonomialOutput.messages.get(key, "No message exists for this type")

class PolynomialOutput():
    #Polynomial related return values
    messages = {
        'POLYNOMIAL_IS_MONOMIAL':"Expression is also a monomial",
        'EXPANDED_MONOMIALS':"Monomials in expression are expanded",
        'FACTORED_POLYNOMIAL':"Expression is fully factored!",
        'NOT_FACTORED_POLYNOMIAL':"Expression is not fully factored",
        'NOT_MONOMIAL':"One or more terms is not a proper monomial",
        'NOT_EXPANDED':"Expression is not fully expanded"
    }

    @staticmethod
    def strout(key):
        return PolynomialOutput.messages.get(key, "No message exists for this type")

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+PolynomialOutput.messages.get(key, "No message exists for this type")

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
        'INVERSE_N':"Expression is raised to -1",
        'CONST_DIVISIBLE':"One or more terms can be combined",
        'NOT_CONST_DIVISIBLE':"Terms cannot be combined by constants",
        'TRIG_CAN_SIMPLIFY':"Can be simplified by a trig identity",
        'TRIG_CANT_SIMPLIFY':"Can't be simplified by trig identities"
    }

    @staticmethod
    def strout(key):
        return UtilOutput.messages.get(key, "No message exists for this type")

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+UtilOutput.messages.get(key, "No message exists for this type")

class ErrorOutput:
    #Error related return values
    messages = {
        'ERROR': "If you see this, we goofed. Email us!"
    }

    @staticmethod
    def strout(key):
        return ErrorOutput.messages.get(key, "No error exists for this type")

    @staticmethod
    def exprstrout(key, expr):
        return srepr(expr)+" "+ErrorOutput.messages.get(key, "No error exists for this type")
