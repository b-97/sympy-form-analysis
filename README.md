# sympy-form-analysis
### Library of Python functions to analyze the form of Sympy expressions

-----

#### Abstract

Proper forms of polynomials are of paramount importance in mathematics research, cryptography, and symbolic computation. While current frameworks to analyze the form of polynomials exist in proprietary computer algebra systems such as Mathematica, an open-source framework is necessary for researchers, educators, and security analysts to evaluate
the code, identify improvements, suggest changes, and distribute freely to
others.

Here we present an open-source framework for supplying standard expressions formed in the Sympy framework with various boolean evaluations on polynomials, including reducibility in various fields and proper forms for singletons, monomials and polynomials. The framework has been built from the ground up for convenient modification, consistent style, and extensive documentation. 

Testing polynomial evaluation for efficiency and accuracy is implemented using Pythons unittest and contexttimer modules. Extending the current offerings of open-source symbolic computation networks allows researchers to use software that respects user freedoms, and we hope that by extending Sympy we can work towards making it a more viable computer algebra system replacement for those in Mathematica, Maple and Matlab.

------
While more methods exist in this library than documented, they are considered incomplete in their current state due to bugs or refactoring issues. Plans are underway to sort them into another testing branch.


#### Library methods:
_(All methods assume the following code has been executed beforehand):_
`import sympy_form_analysis as sfa`

_Proper Singleton Form_

`sfa.is_singleton_form(expr)`

Determines if an expression is a singleton.


_Proper Monomial Form_

`sfa.is_monomial_form(expr)`

Determines whether an expression is in proper monomial form. Monomials are defined as either a singleton or a single product of singletons, where singletons (excluding Rational numbers) are optionally explicitly raised to a power.

_Proper Polynomial Forms_

`sfa.is_fully_expanded_polynomial(expr, eval_trig=False)`

Determines if a SymPy expression is a fully expanded polynomial. A polynomial that is fully expanded is defined in this library as a sum of linearly independent monomials that cannot be expanded further. Eval_trig currently exists for compatibility with earlier versions of sympy-form-analysis, but is currently not in use as features are in development for that flag.

`sfa.is_fully_factored_polynomial(expr, eval_trig=False, domain="RR")`

Determines if a Sympy expression is fully reduced. A polynomial that is fully reduced is defined in this library as an expression that is either a fully reduced polynomial or a product of independent reduced polynomials. By default, sympy-form-analysis determines reducibility for polynomials in the Real domain, however CC, ZZ, and QQ are also supported by specifying the flag as a string. Alternatively, specifying the domains as reals themselves themselves is supported as well.

Testing:

Run tests with:

`python -m sympy-form-analysis.form_test_speed`

or

`python -m sympy-form-analysis.form_test_accuracy`
