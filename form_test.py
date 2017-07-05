from singleton_form import *
from monomial_form import *
from polynomial_form import *
from sympy import *

import unittest
'''
    NOTE: Sympy doesn't honor expression flag evaluate=False
        for the identity property. This may be a crippling problem, that needs
        to be handled by whatever implements this library
        Test a12 has been left in there just in case the issue is resolved
'''
class TestSymp(unittest.TestCase):
    def setUp(self):
        self.x, self.y, self.z  = symbols('x y z')
        self.a1 = Pow(self.x, 2)
        self.a2 = Add(self.x, self.y,evaluate=False)
        self.a3 = Mul(self.x,self.y,2,3,evaluate=False)
        self.a4 = Mul(Pow(self.x,3),self.y,4,evaluate=False)
        self.a5 = Pow(3, 5,evaluate=False)
        self.a6 = Pow(3, pi,evaluate=False)
        self.a7 = Mul(Pow(self.x,4),Pow(self.x,9),evaluate=False)
        self.a8 = Mul(Pow(self.y,3),Pow(self.x,2),evaluate=False)
        self.a9 = Mul(Pow(self.y,pi),Pow(self.x,10),evaluate=False)
        self.a10 = Add(3,pi,pi,evaluate=False)
        self.a11 = Add(1,9,pi,evaluate=False)
        #self.a12 = Add(0,1,evaluate=False)
        self.a13 = Add(152, pi,evaluate=False)
        self.a14 = Add(3, pi,evaluate=False)
        self.a15 = Add(3, Mul(4, pi),evaluate=False)
        self.a16 = Mul(3,pi,evaluate=False)
        self.a17 = Mul(Pow(self.x,3),Pow(self.y,2),self.z,Pow(2,-1),evaluate=False)
        self.a18 = Mul(Mul(Pow(self.x,3),Pow(self.y,2),self.z),Pow(2,-1,evaluate=False),evaluate=False)
        self.a19 = Mul(Pow(Integer(2), Integer(-1)), Pow(Symbol('m'), Integer(2)),evaluate=False)
        self.a20 = sin(self.x)
        self.a21 = Mul(sin(self.x),3,Pow(2,-1,evaluate=False),evaluate=False)
        self.a22 = Add(Pow(self.x,4),Pow(self.x,3),Pow(self.x,2),self.x,1,evaluate=False)
        self.a23 = Add(Mul(2,pi),Mul(3,pi),evaluate=False)
        self.a24 = Pow(Add(self.x,1),2,evaluate=False)
        self.a25 = Mul(3,Add(3,self.x),evaluate=False) #N

    def test_singleton(self):
        self.assertTrue(is_singleton_form(self.x)[0])
        self.assertTrue(is_singleton_form(self.y)[0])
        self.assertTrue(is_singleton_form(self.z)[0])
        self.assertFalse(is_singleton_form(self.a1)[0])
        self.assertFalse(is_singleton_form(self.a2)[0])
        self.assertFalse(is_singleton_form(self.a3)[0]) #N
        self.assertFalse(is_singleton_form(self.a4)[0])
        self.assertFalse(is_singleton_form(self.a5)[0]) #N
        self.assertFalse(is_singleton_form(self.a6)[0])
        self.assertFalse(is_singleton_form(self.a7)[0])
        self.assertFalse(is_singleton_form(self.a8)[0])
        self.assertFalse(is_singleton_form(self.a9)[0])
        self.assertFalse(is_singleton_form(self.a10)[0]) #N
        self.assertFalse(is_singleton_form(self.a11)[0]) #N
        #self.assertFalse(is_singleton_form(self.a12)[0]) #N
        self.assertTrue(is_singleton_form(self.a13)[0])
        self.assertTrue(is_singleton_form(self.a14)[0]) 
        self.assertTrue(is_singleton_form(self.a15)[0])
        self.assertTrue(is_singleton_form(self.a16)[0])
        self.assertFalse(is_singleton_form(self.a17)[0])
        self.assertFalse(is_singleton_form(self.a18)[0])
        self.assertFalse(is_singleton_form(self.a19)[0])
        self.assertTrue(is_singleton_form(self.a20)[0])
        self.assertFalse(is_singleton_form(self.a21)[0])
        self.assertFalse(is_singleton_form(self.a22)[0])
        self.assertFalse(is_singleton_form(self.a23)[0]) #N
        self.assertFalse(is_singleton_form(self.a24)[0])
        self.assertFalse(is_singleton_form(self.a25)[0]) #N

    def test_expanded_monomial(self):
        self.assertTrue(is_monomial_form(self.x)[0])
        self.assertTrue(is_monomial_form(self.y)[0])
        self.assertTrue(is_monomial_form(self.z)[0])
        self.assertTrue(is_monomial_form(self.a1)[0])
        self.assertFalse(is_monomial_form(self.a2)[0])
        self.assertFalse(is_monomial_form(self.a3)[0]) #N
        self.assertTrue(is_monomial_form(self.a4)[0])
        self.assertFalse(is_monomial_form(self.a5)[0]) #N
        self.assertTrue(is_monomial_form(self.a6)[0])
        self.assertFalse(is_monomial_form(self.a7)[0])
        self.assertTrue(is_monomial_form(self.a8)[0])
        self.assertTrue(is_monomial_form(self.a9)[0])
        self.assertFalse(is_monomial_form(self.a10)[0]) #N
        self.assertFalse(is_monomial_form(self.a11)[0]) #N
        #self.assertFalse(is_monomial_form(self.a12)[0]) #N
        self.assertTrue(is_monomial_form(self.a13)[0])
        self.assertTrue(is_monomial_form(self.a14)[0]) 
        self.assertTrue(is_monomial_form(self.a15)[0])
        self.assertTrue(is_monomial_form(self.a16)[0])
        self.assertTrue(is_monomial_form(self.a17)[0])
        self.assertTrue(is_monomial_form(self.a18)[0])
        self.assertTrue(is_monomial_form(self.a19)[0])
        self.assertTrue(is_monomial_form(self.a20)[0])
        self.assertTrue(is_monomial_form(self.a21)[0])
        self.assertFalse(is_monomial_form(self.a22)[0])
        self.assertFalse(is_monomial_form(self.a23)[0]) #N
        self.assertFalse(is_monomial_form(self.a24)[0])
        self.assertFalse(is_monomial_form(self.a25)[0]) #N

    def test_expanded_polynomial(self):
        self.assertTrue(is_fully_expanded_polynomial(self.x)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.y)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.z)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a1)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a2)[0])
        self.assertFalse(is_fully_expanded_polynomial(self.a3)[0]) #N
        self.assertTrue(is_fully_expanded_polynomial(self.a4)[0])
        self.assertFalse(is_fully_expanded_polynomial(self.a5)[0]) #N
        self.assertTrue(is_fully_expanded_polynomial(self.a6)[0])
        self.assertFalse(is_fully_expanded_polynomial(self.a7)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a8)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a9)[0])
        self.assertFalse(is_fully_expanded_polynomial(self.a10)[0]) #N
        self.assertFalse(is_fully_expanded_polynomial(self.a11)[0]) #N
        #self.assertFalse(is_fully_expanded_polynomial(self.a12)[0]) #N
        self.assertTrue(is_fully_expanded_polynomial(self.a13)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a14)[0]) 
        self.assertTrue(is_fully_expanded_polynomial(self.a15)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a16)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a17)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a18)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a19)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a20)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a21)[0])
        self.assertTrue(is_fully_expanded_polynomial(self.a22)[0])
        self.assertFalse(is_fully_expanded_polynomial(self.a23)[0]) #N
        self.assertFalse(is_fully_expanded_polynomial(self.a24)[0])
        self.assertFalse(is_fully_expanded_polynomial(self.a25)[0]) #N
    
    def test_factored_polynomial(self):
        self.assertTrue(is_fully_factored_polynomial(self.x)[0])
        self.assertTrue(is_fully_factored_polynomial(self.y)[0])
        self.assertTrue(is_fully_factored_polynomial(self.z)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a1)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a2)[0])
        self.assertFalse(is_fully_factored_polynomial(self.a3)[0]) #N
        self.assertTrue(is_fully_factored_polynomial(self.a4)[0])
        self.assertFalse(is_fully_factored_polynomial(self.a5)[0]) #N
        self.assertTrue(is_fully_factored_polynomial(self.a6)[0])
        self.assertFalse(is_fully_factored_polynomial(self.a7)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a8)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a9)[0])
        self.assertFalse(is_fully_factored_polynomial(self.a10)[0]) #N
        self.assertFalse(is_fully_factored_polynomial(self.a11)[0]) #N
        #self.assertFalse(is_fully_factored_polynomial(self.a12)[0]) #N
        self.assertTrue(is_fully_factored_polynomial(self.a13)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a14)[0]) 
        self.assertTrue(is_fully_factored_polynomial(self.a15)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a16)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a17)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a18)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a19)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a20)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a21)[0])
        self.assertFalse(is_fully_factored_polynomial(self.a22)[0])
        self.assertFalse(is_fully_factored_polynomial(self.a23)[0]) #N
        self.assertTrue(is_fully_factored_polynomial(self.a24)[0])
        self.assertTrue(is_fully_factored_polynomial(self.a25)[0]) #N

if __name__ == '__main__':
    unittest.main()
