# We worked together for this assignment --Seiju Hirose and Kevin Peng

import numpy as np

def func1(x): # takes in a 2D numpy array
    return x[0]**2 + x[1]**2

def dfunc1(x): # takes in a 2D numpy array
    return np.array([2*x[0], 2*x[1]])

def func2(x): # takes in a 2D numpy array
    return (10**6)*(x[0]**2) + x[1]**2

def dfunc2(x): # takes in a 2D numpy array
    return np.array([2*(10**6)*x[0], 2*x[1]])

def func3(x): # takes in a 5D numpy array
    return x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2 + x[4]**2

def dfunc3(x): # takes in a 5D numpy array
    return np.array([2*x[0], 2*x[1], 2*x[2], 2*x[3], 2*x[4]])


def gradientDescent (func, dfunc, x0, alpha, iternum=100, tol=10**(-10)):
    # fx = func(x0)
    gradf = dfunc(x0)
    norm = tol * 1.1 # so we always enter the while loop (norm > tol assuming tol is positive)
    lst = [x0]

    while iternum>0 and norm>tol:
        # calculate new x and append to the list 
        x1 = x0 - alpha*gradf 
        lst.append(x1)

        # calculate new grad and update x
        gradf = dfunc(x1)
        norm = np.linalg.norm(x1-x0)
        x0 = x1

        # update iternum
        iternum -= 1 

    return lst

# unfinished
# 
def gradientDescent_BT (func, dfunc, x0, alpha, c1, rho, iternum=100, tol=10**(-10)):
    fx = func(x0)
    gradf = dfunc(x0)
    norm = tol * 1.1  # so we always enter the while loop (norm > tol assuming tol is positive)

    while iternum>0 and norm>tol:
        # contracting alpha
        while func(x0-alpha*gradf) > fx - c1*alpha*(gradf@gradf):
            alpha = rho*alpha
            print("alpha:", alpha)

        # calculate new x and append to the list 
        x1 = x0 - alpha*gradf 

        # calculate new grad and update x
        gradf = dfunc(x1)
        norm = np.linalg.norm(x1-x0)
        x0 = x1

        # update iternum
        iternum -= 1 

    return x1


"""
Main
"""
if __name__ == "__main__":
    answer = gradientDescent(func, dfunc, np.array([5, 5]), 0.2)
    print("Number of iterations performed:", len(answer))
    print(answer[-1])
    #print("Function values: ")
    # for x in answer:
    #     print(func(x))

    answer = gradientDescent_BT(func, dfunc, np.array([5, 5]), 1, 0.5, 0.99)
    print(answer)

    