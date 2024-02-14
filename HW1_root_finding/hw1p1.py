# We worked together for this assignment --Seiju Hirose and Kevin Peng

# Function definitions
def bisect(func, x0, x1, iternum=100, tol=10**(-10)):
    # function evaluation
    f0 = func(x0)
    f1 = func(x1)

    # check for different signs
    if f0*f1 >= 0:
        print("Two points have the same sign.")
        return None
    
    # continue
    m = (x0 + x1)/2
    fm = func(m)

    # base case: check for iteration number and tolerance
    if iternum == 0 or abs(fm)<tol:
        return m
    
    # recursive case
    if fm*f0 < 0:
        return bisect(func, x0, m, iternum-1)
    elif fm*f1 < 0:
        return bisect(func, m, x1, iternum-1)
    else:
        return m


def newton(func, dfunc, x, iternum = 100, tol=10**(-10)):
    # function evaluation
    fx = func(x)
    dfx = dfunc(x)

    # check denominator
    if dfx == 0:
        print("Division by zero")
        return None
    
    # calculate x1
    x1 = x - (fx/dfx)

    # base case: check for iteration number and tolerance
    if iternum==0 or x1==x or abs(func(x1))<tol:
        return x1

    # recursive case
    return newton(func, dfunc, x1, iternum-1)


def secant(func, x0, x1, iternum=100, tol=10**(-10)):
    # function evaluation
    f0 = func(x0)
    f1 = func(x1)

    # base case
    if f0==0:
        return x0
    if f1==0:
        return x1

    # check denominator
    diff = f1-f0
    if (diff)==0:
        if x0==x1: # for cases where x0 and x1 converge to the correct root
            return x0
        else: # for cases where x0 and x1 happen to have the same function value
            print("Division by zero")
            return None
        
    # calculate x2
    x2 = x1 - f1*(x1-x0)/(diff)

    # check iteration number and tolerance
    if iternum==0 or abs(func(x2))<tol:
        return x2

    # recursive case
    return secant(func, x1, x2, iternum-1)



if __name__ == "__main__":

    import math

    # Question 0
    def func0(x): 
        return (2*x-1)

    def dfunc0 (x): # derivative of func0
        return 2

    # Question 1
    def func1(x):
        return x**3 - 3*x + 1
    # a: find the root in [1, 2]
    # b: find the root in [0, 1]

    def dfunc1 (x): # derivative of func1
        return 3*x**2 - 3

    # Questioin 2
    def func2a(x):
        return x**2 - 2
    def dfunc2a (x): # derivative of func2a
        return 2*x

    def func2b(x):
        return x**2 - 3
    def dfunc2b (x): # derivative of func2b
        return 2*x

    # Question 3
    def func3(x):
        return math.cos(x)-x
    def dfunc3 (x): # derivative of func3
        return -math.sin(x)-1
    
    ######################## Answers ########################

    # Question 0
    print("Question 0")
    
    print("Bisection method:", bisect(func0, -2, 4))
    print("Newton's method:", newton(func0, dfunc0, 0))
    print("Secant method:", secant(func0, -2, 4))
    print()

    # Question 1
    print("Question 1(a)")
    print("Bisection method:", bisect(func1, 1, 2))
    print("Newton's method:", newton(func1, dfunc1, 2))
    print("Secant method:", secant(func1, 1, 2))
    print()

    print("Question 1(b)")
    print("Bisection method:", bisect(func1, 0, 1))
    print("Newton's method:", newton(func1, dfunc1, 0))
    print("Secant method:", secant(func1, 0, 1))
    print()

    # Question 2
    print("Question 2(a)")
    print("Bisection method:", bisect(func2a, 1, 2))
    print("Newton's method:", newton(func2a, dfunc2a, 2))
    print("Secant method:", secant(func2a, 1, 2))
    print()

    print("Question 2(b)")
    print("Bisection method:", bisect(func2b, 1, 2))
    print("Newton's method:", newton(func2b, dfunc2b, 2))
    print("Secant method:", secant(func2b, 1, 2))
    print()

    # Question 3
    print("Question 3")
    print("Bisection method:", bisect(func3, 0, 2))
    print("Newton's method:", newton(func3, dfunc3, 2))
    print("Secant method:", secant(func3, 1, 2))
