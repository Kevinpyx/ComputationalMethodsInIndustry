# We worked together for this assignment --Seiju Hirose and Kevin Peng

# Function definitions

def bisect(func, x0, x1, iternum=1000, tol=10**(-14)):
    lst = []
    fm = 1 # just so the while loop runs at least once

    while iternum > 0 and abs(fm)>tol:
        iternum -= 1
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
        # append new guess to the list
        lst.append(m)
    
        # recursive case
        if fm*f0 < 0:
            #return bisect(func, x0, m, iternum-1)
            x1 = m
        elif fm*f1 < 0:
            #return bisect(func, m, x1, iternum-1)
            x0 = m
        else:
            return lst

    return lst


def newton(func, dfunc, x, iternum = 1000, tol=10**(-14)):
    lst = [x]

    fx = func(x)

    while iternum > 0 and abs(fx)>tol:
        iternum -= 1

        # function evaluation
        fx = func(x)
        dfx = dfunc(x)

        # check denominator
        if dfx == 0:
            print("Division by zero")
            return None
    
        # calculate x1
        x1 = x - (fx/dfx)
        # append new guess to the list
        lst.append(x1)

        x = x1

    return lst


def secant(func, x0, x1, iternum=1000, tol=10**(-14)):
    lst = [x1]

    f0 = func(x0)
    f1 = func(x1)

    # if f0 or f1 is 0
    if f0==0:
        lst.append(x0)
        return lst
    if f1==0:
        lst.append(x1)
        return lst

    while iternum > 0 and abs(f1)>tol:
        iternum -= 1

        # function evaluation
        f0 = func(x0)
        f1 = func(x1)


        # check denominator
        diff = f1-f0
        if (diff)==0:
            if x0==x1: # for cases where x0 and x1 converge to the correct root
                lst.append(x0)
                return lst
            else: # for cases where x0 and x1 happen to have the same function value
                print("Division by zero")
                return None
        
        # calculate x2
        x2 = x1 - f1*(x1-x0)/(diff)
        lst.append(x2)

        # update the values
        x0 = x1
        x1 = x2

    return lst

"""
lst2err: takes in a list of values and compute the errors of the values with 1 (the solution we know for the two functions here)

lst: a list of values that converge to the solution

Returns a list of same size of errors
"""

def lst2err(lst):
    sol = 1
    return [abs(x - sol) for x in lst]

"""
Main
"""
if __name__ == "__main__":

    import math
    import matplotlib.pyplot as plt

    # 1
    def func1(x):
        return (x-1)*(x-2)*(x-3)

    def dfunc1(x):
        return 3*(x**2) - 12*x + 11

    # 2
    def func2(x):
        return (x-1)**3
    
    def dfunc2(x):
        return 3*((x-1)**2)

    # function 1

    # print("Bisection: \n", bisect(func1, 0.4, 1.9))
    # print("Newton: \n", newton(func1, dfunc1, 0.1))
    # print("Secant: \n", secant(func1, 0.4, 0.6))
    
    # calculate errors
    bisectionError = lst2err(bisect(func1, 0.9, 1.9))
    newtonError = lst2err(newton(func1, dfunc1, 0.1))
    secantError = lst2err(secant(func1, 0.4, 0.6))

    # print("Bisection: \n", bisectionError)
    # print("Newton: \n", newtonError)
    # print("Secant: \n", secantError)

    # plot errors
    plt.subplot(1, 2, 1)  # row 1, column 2, count 1
    plt.title('f(x)=(x-1)(x-2)(x-3)')
    plt.loglog(bisectionError[:-1], bisectionError[1:], 'r', label="bisect")
    plt.loglog(newtonError[:-1], newtonError[1:], 'g', label="newton")
    plt.loglog(secantError[:-1], secantError[1:], 'b', label="secant")
    plt.legend(loc="best")
    plt.grid()

    # function 2
    # calculate errors
    bisectionError2 = lst2err(bisect(func2, 0.9, 1.9))
    newtonError2 = lst2err(newton(func2, dfunc1, 0.1))
    secantError2 = lst2err(secant(func2, 0.4, 0.6))

    # print("Bisection: \n", bisectionError2)
    # print("Newton: \n", newtonError2)
    # print("Secant: \n", secantError2)

    # plot errors
    plt.subplot(1, 2, 2)
    plt.title('f(x)=(x-1)^3')
    plt.loglog(bisectionError2[:-1], bisectionError2[1:], 'r', label="bisect")
    plt.loglog(newtonError2[:-1], newtonError2[1:], 'g', label="newton")
    plt.loglog(secantError2[:-1], secantError2[1:], 'b', label="secant")

    plt.legend(loc="best")
    plt.grid()

    plt.show()

"""
Observations:
With the first function (left subplot), all three methods are roughly a straighline with 
constant slope. With the second function (right subplot), however, newton's method is
having trouble converging efficiently.
"""
