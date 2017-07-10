class FormOutput:
    #Singleton related return values
    IMPROPER_SINGLETON_TERM = "Improper term in singleton"
    REDUCIBLE_SINGLETON = "Singleton can be reduced"
    INVALID_SINGLETON_PRODUCT = "Invalid product in singleton"
    INVALID_SINGLETON_SUM = "More than one term in singleton"
    VALID_SINGLETON_SUM = "Valid summation in singleton"

    VALID_SINGLETON = "Expression is a singleton"
    VALID_SINGLETON_PRODUCT = "Appropriate product for singleton"
    VALID_SINGLETON_TRIG = "Expression is a trig function"
    VALID_SINGLETON_INVTRIG = "Expression is an inverse trig function"

    INVALID_SINGLETON = "Not a singleton"

    #Monomial related return values
    REDUCIBLE_MONOMIAL = "Monomial is reducible"
    EXPANDABLE_MONOMIAL = "One or more monomials could be expanded"
    PROPER_MONOMIAL = "Expression is a proper monomial"
    IMPROPER_MONOMIAL = "Expression is not a proper monomial"
    MONOMIAL_IS_SINGLETON = "Monomial is also a singleton"
    MONOMIAL_MULTIPLE_TERMS = "More than 1 term in monomial"

    #Polynomial related return values
    POLYNOMIAL_IS_MONOMIAL = "Expression is also a monomial"
    EXPANDED_MONOMIALS = "Monomials in expression are expanded"
    FACTORED_POLYNOMIAL = "Expression is fully factored!"
    NOT_FACTORED_POLYNOMIAL = "Expression is not fully factored"
    NOT_MONOMIAL = "One or more terms is not a proper monomial"
    NOT_EXPANDED = "Expression is not fully expanded"

    #Utility related return values
    SIMPLIFIABLE_NUMERATOR = "Numerator can be simplified"
    SIMPLIFIABLE_DENOMINATOR = "Denominator can be simplified"

    SIMPLIFIABLE_FRACTION = "Terms in fraction can be cancelled"
    NOT_SIMPLIFIABLE_FRACTION = "No terms can be cancelled in fraction"

    CONST_TO_CONST = "Expression is a constant raised to a constant"
    NOT_CONST_TO_CONST = "Expression isn't a constant raised to a constant"
    ONE_OVER_N = "Expression is raised to 1/n"
    INVERSE_N = "Expression is raised to -1"

    CONST_DIVISIBLE = "One or more terms can be combined"
    NOT_CONST_DIVISIBLE = "Terms cannot be combined by constants"

    TRIG_CAN_SIMPLIFY = "Can be simplified by a trig identity"
    TRIG_CANT_SIMPLIFY = "Can't be simplified by trig identities"

    ERROR = "If you see this, we goofed. Email us!"
