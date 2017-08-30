# sympy-form-analysis
### Library of Python functions to analyze the form of Sympy expressions

Proper forms of polynomials are of paramount importance in mathematics research, cryptography, and symbolic computation. While current frameworks to analyze the form of polynomials exist in proprietary computer algebra systems such as Mathematica, an open-source framework is necessary for researchers, educators, and security analysts to evaluate
the code, identify improvements, suggest changes, and distribute freely to
others.

Here we present an open-source framework for supplying standard expressions formed in the Sympy framework with various boolean evaluations on polynomials, including reducibility in various fields and proper forms for singletons, monomials and polynomials. The framework has been built from the ground up for convenient modification, consistent style, and extensive documentation. 

Testing polynomial evaluation for efficiency and accuracy is implemented using Pythons unittest and contexttimer modules. Extending the current offerings of open-source symbolic computation networks allows researchers to use software that respects user freedoms, and we hope that by extending Sympy we can work towards making it a more viable computer algebra system replacement for those in Mathematica, Maple and Matlab.

Testing:
Run tests with:
`python -m sympy-form-analysis.form_test_speed
or
`python -m sympy-form-analysis.form_test_accuracy
