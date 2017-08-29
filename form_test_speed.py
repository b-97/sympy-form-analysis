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
import random

'''
    NOTE: Sympy doesn't honor expression flag evaluate=False
        for the identity property. This may be a crippling problem, that needs
        to be handled by whatever implements this library
        Test a12 has been left in there just in case the issue is resolved
'''
gen_exprs = []

test_poly_deg = 2

for i in range(500):
    randcoeffs = [0]
    while(randcoeffs[0] == 0):
        randcoeffs = np.random.choice(range(1000),test_poly_deg,replace=True)

    randpoly = Poly(randcoeffs,x,domain=RR)
    gen_exprs.append(randpoly.as_expr())
    
    test_poly_deg += 1
    if(test_poly_deg > 21):
        test_poly_deg = 2

if not os.path.exists("test_results"):
        os.makedirs("test_results")

class TestSymp(unittest.TestCase):
    def setUp(self):
        self.total_exprs = gen_exprs
    '''
    def test_singleton_speed(self):
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
        plt.scatter(np.array(list_x), np.array(list_y),color="red")
        plt.title("is_singleton_form(expr)")
        plt.xlabel("Polynomial Length")
        plt.ylabel("Evaluation Time (ms)")
        plt.savefig('test_results/singleton.png', bbox_inches='tight')
        plt.clf()

    def test_monomial_speed(self):
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/monomial.csv","w+")
        list_x = []
        list_y = []
        for i in self.total_exprs:
            leng = polynomial_length(i)
            list_x.append(leng)
            with Timer(factor=1000) as t:
                is_monomial_form(i)
            time = t.elapsed
            f.write(str(leng)+","+str(time)+"\n")
            list_y.append(time)
        f.close()
        plt.scatter(np.array(list_x), np.array(list_y),color="orangered")
        plt.title("is_monomial_form(expr)")
        plt.xlabel("Polynomial Length")
        plt.ylabel("Evaluation Time (ms)")
        plt.savefig('test_results/monomial.png', bbox_inches='tight')
        plt.clf()
   
    '''
    def test_expanded_polynomial_speed(self):
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/expanded_poly.csv","w+")
        list_x = []
        list_y = []
        for i in self.total_exprs:
            #leng = polynomial_length(i)
            deg = degree(i)
            #list_x.append(leng)
            list_x.append(deg)
            with Timer(factor=1000) as t:
                is_fully_expanded_polynomial(i)
            time = t.elapsed
            #f.write(str(leng)+","+str(time)+"\n")
            f.write(str(deg)+","+str(time)+"\n")
            list_y.append(time)
        f.close()
        plt.scatter(np.array(list_x), np.array(list_y),color="darkkhaki")
        plt.title("is_fully_expanded_polynomial(expr)")
        plt.xlabel("Polynomial Length")
        plt.ylabel("Evaluation Time (ms)")
        plt.savefig('test_results/expanded_poly.png', bbox_inches='tight')
        plt.clf()

    '''
    def test_complex_factored_speed(self):
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/complex_factored.csv","w+")
        list_x = []
        list_y = []
        for i in self.total_exprs:
            deg = degree(i)
            list_x.append(deg)
            with Timer(factor=1000) as t:
                is_fully_factored_polynomial(i,domain="CC")
            time = t.elapsed
            f.write(str(deg)+","+str(time)+"\n")
            list_y.append(time)
        f.close()
        plt.scatter(np.array(list_x), np.array(list_y),color="darkgreen")
        plt.title("is_fully_factored_polynomial_form(expr,domain=\"CC\")")
        plt.xlabel("Polynomial Degree")
        plt.ylabel("Evaluation Time (ms)")
        plt.savefig('test_results/complex_factored.png', bbox_inches='tight')
        plt.clf()

    def test_real_factored_speed(self):
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/real_factored.csv","w+")
        list_x = []
        list_y = []
        for i in self.total_exprs:
            deg = degree(i)
            list_x.append(deg)
            with Timer(factor=1000) as t:
                is_fully_factored_polynomial(i,domain="RR")
            time = t.elapsed
            f.write(str(deg)+","+str(time)+"\n")
            list_y.append(time)
        f.close()
        plt.scatter(np.array(list_x), np.array(list_y),color="teal")
        plt.title("is_fully_factored_polynomial_form(expr,domain=\"RR\")")
        plt.xlabel("Polynomial Degree")
        plt.ylabel("Evaluation Time (ms)")
        plt.savefig('test_results/real_factored.png', bbox_inches='tight')
        plt.clf()

    def test_rational_factored_speed(self):
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/rational_factored.csv","w+")
        list_x = []
        list_y = []
        for i in self.total_exprs:
            leng = polynomial_length(i)
            list_x.append(leng)
            with Timer(factor=1000) as t:
                is_fully_factored_polynomial(i,domain="QQ")
            time = t.elapsed
            f.write(str(leng)+","+str(time)+"\n")
            list_y.append(time)
        f.close()
        plt.scatter(np.array(list_x), np.array(list_y),color="blue")
        plt.title("is_fully_factored_polynomial_form(expr,domain=\"QQ\")")
        plt.xlabel("Polynomial Degree")
        plt.ylabel("Evaluation Time (ms)")
        plt.savefig('test_results/rational_factored.png', bbox_inches='tight')
        plt.clf()

    def test_integer_factored_speed(self):
        os.environ["SYMPY_USE_CACHE"] = "no"
        f = open("test_results/integer_factored.csv","w+")
        list_x = []
        list_y = []
        for i in self.total_exprs:
            leng = polynomial_length(i)
            list_x.append(leng)
            with Timer(factor=1000) as t:
                is_fully_factored_polynomial(i,domain="ZZ")
            time = t.elapsed
            f.write(str(leng)+","+str(time)+"\n")
            list_y.append(time)
        f.close()
        plt.scatter(np.array(list_x), np.array(list_y),color="violet")
        plt.title("is_fully_factored_polynomial_form(expr,domain=\"QQ\")")
        plt.xlabel("Polynomial Size")
        plt.ylabel("Evaluation Time (ms)")
        plt.savefig('test_results/integer_factored.png', bbox_inches='tight')
        plt.clf()
    '''

if __name__ == '__main__':
    unittest.main()
