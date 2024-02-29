# We worked together for this assignment --Seiju Hirose and Kevin Peng

import numpy as np
import math
import matplotlib.pyplot as plt

##### Test Functions #####

def func1(x): # takes in a 2D numpy array
    return x[0]**2 + x[1]**2

def dfunc1(x): # takes in a 2D numpy array
    return np.array([2*x[0], 2*x[1]])

def d2func1(x):
    return np.array([[2, 0], [0, 2]])

def func2(x): # takes in a 2D numpy array
    return (10**6)*(x[0]**2) + x[1]**2

def dfunc2(x): # takes in a 2D numpy array
    return np.array([2*(10**6)*x[0], 2*x[1]])

def d2func2(x):
    return np.array([[2*(10**6), 0], [0, 2]])

def func3(x): # takes in a 5D numpy array
    return x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2 + x[4]**2

def dfunc3(x): # takes in a 5D numpy array
    return np.array([2*x[0], 2*x[1], 2*x[2], 2*x[3], 2*x[4]])

def d2func3(x): 
    return 2 * np.identity(5)

def func4(x):
    return math.cos(x[0]) + math.sin(x[1])

def dfunc4(x):
    return np.array([-math.sin(x[0]), math.cos(x[1])])

def d2func4(x):
    return np.array([[-math.cos(x[0]), 0], [0, -math.sin(x[1])]])

##### Newton #####
def newton(jacobian, hessian, x, iternum = 100, tol=10**(-14)):
    lst = [x]

    fx = jacobian(x)
    error = abs(np.linalg.norm(fx))

    while iternum > 0 and error>tol:
        iternum -= 1

        # function evaluation
        dfx = hessian(x)
    
        # calculate x1
        x1 = x - np.linalg.inv(dfx)@fx
        # append new guess to the list
        lst.append(x1)

        x = x1
        fx = jacobian(x)
        error = abs(np.linalg.norm(fx))

    return lst

def lst2err(lst, solution):
    return [abs(x - solution) for x in lst]

"""
Main
"""
if __name__ == "__main__":
    ### Question 1 ###
    print()
    print("f1:")
    answer = newton(dfunc1, d2func1, np.array([5, 5]))
    print("Number of iterations performed:", len(answer)-1)
    print(answer[-1])

    print()
    print("f2:")
    answer = newton(dfunc2, d2func2, np.array([5, 5]))
    print("Number of iterations performed:", len(answer)-1)
    print(answer[-1])

    print()
    print("f3:")
    answer = newton(dfunc3, d2func3, np.array([5, 5, 5, 5, 5]))
    print("Number of iterations performed:", len(answer)-1)
    print(answer[-1])

    print()
    print("f4:")
    answer = newton(dfunc4, d2func4, np.array([3, 4]))
    print("Number of iterations performed:", len(answer)-1)
    print(answer[-1])
    print(answer)

    # calculating errors of norms
    norms = [np.linalg.norm(x) for x in answer]
    errors = lst2err(norms, np.linalg.norm(np.array([math.pi, math.pi*3/2])))

    plt.subplot(1, 2, 1)
    plt.title('f4: norm convergence analysis')
    plt.loglog(errors[:-1], errors[1:])
    plt.grid()

    # calculating errors of x1 and x2 values
    x1_lst = [v[0] for v in answer]
    x2_lst = [v[1] for v in answer]
    x1_err = lst2err(x1_lst, math.pi)
    x2_err = lst2err(x2_lst, math.pi*3/2)

    plt.subplot(1, 2, 2)
    plt.title('f4: x1 and x2 convergence analysis')
    plt.loglog(x1_err[:-1], x1_err[1:], 'b', label="x1")
    plt.loglog(x2_err[:-1], x2_err[1:], 'g', label="x2")
    plt.legend(loc="best")
    plt.grid()

    plt.show()