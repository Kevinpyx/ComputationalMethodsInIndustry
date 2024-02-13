import math

"""
newton: Newton's method

func: the function f we optimize on
dfunc: the derivative df/dx
x: the current solution
iternum: number of iterations. After 100 iterations, newton stops.
tol: tolerance value. If x is close enough to the true solution, i.e. the distance between is less than tol, newton stops.
"""
def newton(func, dfunc, x, iternum = 100, tol=10**(-10)):
    fx = func(x)
    dfx = dfunc(x)
    if dfx == 0:
        print("Division by zero")
        return None
    
    # calculate new solution based on x
    x1 = x - (fx/dfx)


    # base case
    if iternum==0 or x1==x or abs(func(x1))<tol:
        return x1

    # recursive
    return newton(func, dfunc, x1, iternum-1)

"""
Main
"""
if __name__ == "__main__":
    
    """
    Part 1
    """
    def func4(x):
        return x**3 - 3*x + 1

    def dfunc4(x):
        return 3*x**2 - 3

    print(newton(func4, dfunc4, -0.8))

    """
    Interpretation of the problem:
        The tangent line at -0.8 led us to the right side of root 1.532. Therefore, the function 
        just found the root 1.532, rather than the root between 0 and 1. We can't find the 
        desired root starting with -0.8.
    """

    """
    Part 2
    """
    def func5(x):
        return x**3 - 2*x + 2

    def dfunc5(x):
        return 3*x**2 - 2

    print(newton(func5, dfunc5, 0))
    """
    Interpretation of the problem:
        The tangent line at 0 leads us to root x_1=1. The tangent line at 1 leads us back to 0. 
        So x oscillates between 0 and 1 and never converges. We can't find the desired root starting with 0.
    """

    """
    Part 3
    """
    def func6(x):
        return math.exp(x)/(1+math.exp(x)) - 0.5

    def dfunc6(x):
        return math.exp(x)/((1 + math.exp(x))**2)

    #starting from -3
    print(newton(func6, dfunc6, -3))
    
    #starting from -2
    print(newton(func6, dfunc6, -2))

    """
    Interpretation of the problem:
        The newton's method doesn't work when x_0=-3 but works when x_0=-2. The problem with -3 is 
        the gradient at -3 is too flat so it leads us to a point with greater x (absolute) value, 
        where the gradient is even flatter. And then we get to a point even farther away from the root 
        and lastly there is a math range error because the number goes out of the range. -2 works 
        because the gradient is steep enough for us to converge to 0. 
    """

    """
    Part 4
    """
    def func7(x):
        return math.sin(x) - x

    def dfunc7(x):
        return math.cos(x) - 1

    print(newton(func7, dfunc7, -2*math.pi))

    """
    Interpretation of the problem:
        The Newton method works for most x values except integer multiples of 2π, where the slope becomes 0.
    """

    """
    Part 5
    """
    # (a)
    def func8a(x):
        return abs(x)**(1/3)

    def dfunc8a(x):
        #print("evaluating derivative:", x)

        if x<0:
            # 1/3 * (-x)^(-2/3)
            return -((x**2)**(-1/3))/3
        if x>0:
            return (1/3)*(x**(-2/3))
        else:
            raise Exception("Attempted to evaluate derivative at 0")

    print(newton(func8a, dfunc8a, 1))

    # (b)
    def func8b(x):
        return abs(x)**(2/3)

    def dfunc8b(x):
        #print("evaluating derivative:", x)

        if x<0:
            return 2/3*(-x)**(-1/3)
        if x>0:
            return (2/3)*(x**(-1/3))
        else:
            raise Exception("Attempted to evaluate derivative at 0")
        
    print(newton(func8b, dfunc8b, 1))

    # (c)
    def func8c(x):
        return abs(x)**(4/3)

    def dfunc8c(x):
        #print("evaluating derivative:", x)

        if x<0:
            return 4/3*(-x)**(1/3)
        if x>0:
            return (4/3)*(x**(1/3))
        else:
            raise Exception("Attempted to evaluate derivative at 0")
        
    print(newton(func8c, dfunc8c, 1))

    """
    Interpretation of the problem:
        For (a) and (b), the gradient is too flat so the value diverges. Only (c) converges 
        because the numerator is smaller than the denominator. The others don't converge at all 
        no matter how close from 0 we start. 
    """