from .singleton_form import *
from .monomial_form import *
from .polynomial_form import *
from .numerical_base_form import *
from .equivalent_form import *
from .test_utils import *
from sympy import *
from sympy.abc import x,y,z
import os
import unittest
from contexttimer import Timer
import matplotlib.pyplot as plt
import numpy as np

'''
    NOTE: Sympy doesn't honor expression flag evaluate=False
        for the identity property. This may be a crippling problem, that needs
        to be handled by whatever implements this library
        Test a12 has been left in there just in case the issue is resolved
'''
class TestSymp(unittest.TestCase):
    def setUp(self):
        self.a1 = Pow(x, 2)
        self.a2 = Add(x, y,evaluate=False)
        self.a3 = Mul(x,y,2,3,evaluate=False)
        self.a4 = Mul(Pow(x,3),y,4,evaluate=False)
        self.a5 = Pow(3, 5,evaluate=False)
        self.a6 = Pow(3, pi,evaluate=False)
        self.a7 = Mul(Pow(x,4),Pow(x,9),evaluate=False)
        self.a8 = Mul(Pow(y,3),Pow(x,2),evaluate=False)
        self.a9 = Mul(Pow(y,pi),Pow(x,10),evaluate=False)
        self.a10 = Add(3,pi,pi,evaluate=False)
        self.a11 = Add(1,9,pi,evaluate=False)
        self.a13 = Add(152, pi,evaluate=False)
        self.a14 = Add(3, pi,evaluate=False)
        self.a15 = Add(3, Mul(4, pi),evaluate=False)
        self.a16 = Mul(3,pi,evaluate=False)
        self.a17 = Mul(Pow(x,3),Pow(y,2),z,Pow(2,-1),evaluate=False)
        self.a18 = Mul(Mul(Pow(x,3),Pow(y,2),z),Pow(2,-1,evaluate=False),evaluate=False)
        self.a19 = Mul(Pow(Integer(2), Integer(-1)), Pow(Symbol('m'), Integer(3)),evaluate=False)
        self.a20 = sin(x)
        self.a21 = Mul(sin(x),3,Pow(2,-1,evaluate=False),evaluate=False)
        self.a22 = Add(Pow(x,4),Pow(x,3),Pow(x,2),x,1,evaluate=False)
        self.a23 = Add(Mul(2,pi),Mul(3,pi),evaluate=False)
        self.a24 = Pow(Add(x,1),2,evaluate=False)
        self.a25 = Mul(3,Add(3,x),evaluate=False) #N
        self.a26 = Add(Mul(3,Pow(x,2)),Pow(x,1),5,evaluate=False) #N - Exponent 1
        self.a26 = Add(Mul(3,Pow(x,2)),Pow(x,0),5,evaluate=False) #N - Exponent 0
        self.a27 = Add(Mul(0,Pow(x,2)),Pow(x,0),5,evaluate=False) #N - 0*x
        self.a28 = Mul(2,Pow(4,-1,evaluate=False),evaluate=False) #N - 2/4
        self.a29 = Add(x, Mul(2,Pow(4,-1,evaluate=False),evaluate=False),evaluate=False) #N - x + 2/4
        self.a30 = Add(x, Mul(-1,Pow(3,-1,evaluate=False),evaluate=False))
        self.a31 = Mul(pi,Pow(pi,-1,evaluate=False),evaluate=False) #N - pi/pi
        self.a32 = Mul(pi,Pow(pi,-2,evaluate=False),evaluate=False) #N - pi/pi^2
        self.a33 = Pow(pi,pi,evaluate=False)
        self.a34 = Mul(-1,Pow(pi,pi,evaluate=False),evaluate=False)
        self.a35 = Pow(Mul(-4,pi),pi,evaluate=False)
        self.a36 = Add(x,3,Add(x,2,evaluate=False),evaluate=False)

        #Polynomials from Wikipedia
        self.w1 = Add(Pow(x,2),Mul(4,x),4,evaluate=False) #CC,RR,QQ,ZZ
        self.w2 = Add(Pow(x,2),-4,evaluate=False)

        self.b1 = Mul(Pow(3,5,evaluate=False),Pow(9,10,evaluate=False),evaluate=False)
        self.b2 = Pow(3,5,evaluate=False)
        self.b3 = Pow(9,10,evaluate=False)
        self.b4 = Pow(3,3,evaluate=False)

        self.total_exprs = [x,y,z,self.a1,self.a2,self.a3,self.a4,self.a5,self.a6,
            self.a7,self.a8,self.a9,self.a10,self.a11,self.a13,
            self.a14,self.a15,self.a16,self.a17,self.a18,self.a19,self.a20,
            self.a21,self.a22,self.a23,self.a24,self.a25,self.a26,self.a27,
            self.a28,self.a29,self.a30,self.a31,self.a32,self.a33,self.a34,
            self.a35,self.a36,self.w1,self.w2]

    def test_singleton_speed(self):
        #Turn off caching in python so we don't screw up time results
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/singleton.csv","w+")
        list_x = []
        list_y = []
        for i in self.total_exprs:
            leng = polynomial_length(i)
            list_x.append(leng)
            with Timer(factor=1000) as t:
                is_singleton_form(i)
            time = t.elapsed
            f.write(str(leng)+","+str(time)+"\n")
            list_y.append(time)
        f.close()
        plt.plot(np.array(list_x), np.array(list_y))
        plt.show()

    def test_monomial_speed(self):
        #Turn off caching in python so we don't screw up time results
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/monomial.csv","w+")
        for i in self.total_exprs:
            leng = polynomial_length(i)
            with Timer(factor=1000) as t:
                is_monomial_form(i)
            f.write(str(leng)+","+str(t.elapsed)+"\n")
        f.close()

    def test_expanded_polynomial_speed(self):
        #Turn off caching in python so we don't screw up time results
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/expanded_polynomial.csv","w+")
        for i in self.total_exprs:
            leng = polynomial_length(i)
            with Timer(factor=1000) as t:
                is_fully_expanded_polynomial(i)
            f.write(str(leng)+","+str(t.elapsed)+"\n")
        f.close()

    
    def test_factored_complex_speed(self):
        #Turn off caching in python so we don't screw up time results
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/factored_complex_polynomial.csv","w+")
        for i in self.total_exprs:
            leng = polynomial_length(i)
            with Timer(factor=1000) as t:
                is_fully_factored_polynomial(i,domain='CC')
            f.write(str(leng)+","+str(t.elapsed)+"\n")
        f.close()


    def test_factored_real_speed(self):
        #Turn off caching in python so we don't screw up time results
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/factored_real_polynomial.csv","w+")
        for i in self.total_exprs:
            leng = polynomial_length(i)
            with Timer(factor=1000) as t:
                is_fully_factored_polynomial(i,domain='RR')
            f.write(str(leng)+","+str(t.elapsed)+"\n")
        f.close()

    def test_factored_rational_speed(self):
        #Turn off caching in python so we don't screw up time results
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/factored_rational_polynomial.csv","w+")
        for i in self.total_exprs:
            leng = polynomial_length(i)
            with Timer(factor=1000) as t:
                is_fully_factored_polynomial(i,domain='QQ')
            f.write(str(leng)+","+str(t.elapsed)+"\n")
        f.close()

    def test_factored_integer_speed(self):
        #Turn off caching in python so we don't screw up time results
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/factored_integer_polynomial.csv","w+")
        for i in self.total_exprs:
            leng = polynomial_length(i)
            with Timer(factor=1000) as t:
                is_fully_factored_polynomial(i,domain='ZZ')
            f.write(str(leng)+","+str(t.elapsed)+"\n")
        f.close()
    
if __name__ == '__main__':
    unittest.main()
