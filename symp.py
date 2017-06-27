from sympy import *

#TODO: Complex numbers?
#TODO: Camel case

#Returns whether expression in question is a real number
#to the power of a real number, which could be simplified.
def const_to_const(expr):
    return isinstance(expr, Pow) and \
            isinstance(expr.args[0], Number) and \
            isinstance(expr.args[1], Number)

#Returns if an expression is a singleton.
def is_singleton(expr):
    if isinstance(expr, Number):
        return True
    elif isinstance(expr, NumberSymbol):
        return True
    elif isinstance(expr, Symbol):
        return True
            
    #First: test to see if it's raised to a power
    #If so, make sure the exponent is a constant
    #and make sure the expression inside is singleton-worthy
    if isinstance(expr, Pow):
        #TODO: Add code to pass bases like (pi + 3)
        if isinstance(expr.args[0], Mul):
            return False
        if const_to_const(expr):
            return False
        elif isinstance(expr.args[0], Add):
            return False
        else:
            return True
    
    return False 

#Returns if an expression is a monomial or not.
def is_monomial(expr): 
    if is_singleton(expr):
        return True
    elif not isinstance(expr, Mul):
        return False
    else:
        for i in range(0,len(expr.args)):
            if not is_singleton(expr.args[i]):
                print(srepr(expr))
                return False
    
    return not duplicate_bases(expr)

#Checks to see if the polynomial given is well formed.
def is_polynomial(expr):
    #If the expression is a monomial or a singleton
    if is_monomial(expr):
        return True
    
    #If the monomial test fails with < 2 terms
    elif not isinstance(expr, Add):
        return False

    #Make sure each term in the polynomial is a monomial
    else:
        for i in range(0, len(expr.args)):
            if not is_monomial(expr.args[i]):
                print(srepr(expr))
                return False
    return not duplicate_monomials(expr)

#Test to see if any of the factors are dupes
def duplicate_bases(expr):
    bases = []
    
    #collect the bases - if there's an exponent, just look
    #at the base
    for i in range(0, len(expr.args)):
        if isinstance(expr.args[i], Pow):
            bases.append(expr.args[i].args[0])
        else:
            bases.append(expr.args[i])
    
    #check for any dupes
    return len(bases) != len(set(bases))

#returns if any of the monomials can be combined
def duplicate_monomials(expr):
    monomials = []
    
    #collect the bases if there's an exponent, just look
    #at the base
    for i in range(0, len(expr.args)):
        if isinstance(expr.args[i], Pow):
            monomials.append(expr.args[i].args[0])
        else:
            monomials.append(expr.args[i])
        #Check to see if any of the other monomials
        #are divisible with integer quotient and 0
        #remainder
        if i <= len(expr.args) - 2:
            for j in range(i+1, len(expr.args)):
                if(const_divisible(expr.args[i], expr.args[j])):
                    print(expr.args[i], expr.args[j])
                    return True

    print("what")
    #Check for any duplicates 
    return len(monomials) != len(set(monomials))

#Returns whether division of one expresion into another
#produces any constant without a remainder
def const_divisible(expr1, expr2):
    q, r = div(expr1, expr2, domain='ZZ')
    return isinstance(q, Number) or \
            isinstance(q, NumberSymbol) and \
            r == 0

#returns whether the exponent is a constant or not
def const_expon(expr):
    return isinstance(expr, Pow) and \
        (isinstance(expr.args[1], Number) or \
        isinstance(expr.args[1], NumberSymbol))
