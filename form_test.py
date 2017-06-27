from singleton_form import *
from monomial_form import *
from polynomial_form import *

import unittest
'''
    NOTE: Sympy doesn't honor expression flag evaluate=False
        for the identity property. This may be a crippling problem, that needs
        to be handled by whatever implements this library
'''
class TestSymp(unittest.TestCase):
    def setUp(self):
        self.x = Symbol('x')
        self.y = Symbol('y')
        self.a1 = Pow(self.x, 2, evaluate=False)
        self.a2 = Add(self.x, self.y, evaluate=False)
        self.a3 = Mul(self.x,self.y,2,3, evaluate = False)
        self.a4 = Mul(Pow(self.x,3),self.y,4,evaluate = False)
        self.a5 = Pow(3, 5, evaluate = False)
        self.a6 = Pow(3, pi, evaluate = False)
        self.a7 = Mul(Pow(self.x,4),Pow(self.x,9),evaluate=False)
        self.a8 = Mul(Pow(self.y,3),Pow(self.x,2),evaluate=False)
        self.a9 = Mul(Pow(self.y,pi),Pow(self.x,10),evaluate=False)
        self.a10 = Add(3,pi,pi,evaluate=False)
        self.a11 = Add(1,9,pi,evaluate=False)
        #self.a12 = Add(0,1,evaluate=False)
        self.a13 = Add(152, pi, evaluate=False)
    
    
    
    def test_singleton(self):
        self.assertTrue(is_singleton(self.x))
        self.assertTrue(is_singleton(self.y))
        self.assertTrue(is_singleton(self.a1))
        self.assertFalse(is_singleton(self.a2))
        self.assertFalse(is_singleton(self.a3))
        self.assertFalse(is_singleton(self.a10))
        self.assertFalse(is_singleton(self.a11))
        #self.assertFalse(is_singleton(self.a12))
        self.assertTrue(is_singleton(self.a13))
    
    
    
    def test_monomial(self):
        self.assertTrue(is_monomial(self.x))
        self.assertTrue(is_monomial(self.y))
        self.assertTrue(is_monomial(self.a1))
        self.assertFalse(is_monomial(self.a2))
        self.assertTrue(is_monomial(self.a3))
        self.assertTrue(is_monomial(self.a4))
        self.assertFalse(is_monomial(self.a5))
        self.assertTrue(is_monomial(self.a6))
        self.assertFalse(is_monomial(self.a7))
        self.assertTrue(is_monomial(self.a8))
        self.assertTrue(is_monomial(self.a9))
    
    
    
    def test_polynomial(self):
        self.assertFalse(is_polynomial(self.a10))
        self.assertFalse(is_polynomial(self.a11))
        #self.assertFalse(is_polynomial(self.a12))
        self.assertTrue(is_polynomial(self.a13))
if __name__ == '__main__':
    unittest.main()
