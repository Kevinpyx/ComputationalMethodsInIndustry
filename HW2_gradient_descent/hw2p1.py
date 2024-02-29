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

A = np.array([[2,-1,0],[-1,2,-1],[0,-1,2]] )
b = np.array([2,0,2])
def funcProb1p2(x): # takes in a numpy array
    return 0.5 * x.transpose() @ A @ x - b.transpose() @ x

def dfuncProb1p2(x): # takes in a numpy array
    return A@x - b

# Problem 1: gradientDescent with fixed alpha
def gradientDescent (func, dfunc, x0, alpha, iternum=100, tol=10**(-10)):
    # fx = func(x0)
    gradf = dfunc(x0)
    norm = tol * 1.1 # so we always enter the while loop (norm > tol assuming tol is positive)
    lst = [x0]

    while iternum>0 and norm>tol:
        # calculate new x and append to the list 
        x1 = x0 - alpha*gradf 
        lst.append(x1)

        # calculate new grad and update x0
        gradf = dfunc(x1)
        norm = np.linalg.norm(x1-x0)
        x0 = x1

        # update iternum
        iternum -= 1 

    return lst

# Problem 2
def gradientDescent2 (func, dfunc, x0, iternum=100, tol=10**(-10)):
    # fx = func(x0)
    gradf = dfunc(x0)
    norm = tol * 1.1 # so we always enter the while loop (norm > tol assuming tol is positive)
    lst = [x0]

    print(gradf)

    while iternum>0 and norm>tol:
        # calculate alpha from fixed A and b (Problem 2)
        gradfT = gradf.transpose()
        alpha = (gradfT@gradf)/(gradfT@A@gradf)
        
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
        print("new alpha:", alpha)    

        # calculate new x and append to the list 
        x1 = x0 - alpha*gradf 

        # calculate new grad and update x0
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
    # print()

    ### Question 1 ###
    print("f1 with big step size")
    guesses = gradientDescent(func11, dfunc11, np.array([5, 5]), 2)
    # print("Number of iterations performed:", len(guesses)-1)
    print("Best guess:", guesses[-1])
    # print()
    # print("Every ten guesses:")
    # for n in range(0, len(guesses), 10):
    #     print(guesses[n])
    print()
    # Observation:
    # When the step size is too large, the function oversteps and diverges. 

    print("f1 with small step size")
    guesses = gradientDescent(func1, dfunc1, np.array([5, 5]), 10**(-4))
    # print("Number of iterations performed:", len(guesses)-1)
    print("Best guess:", guesses[-1])
    # print()
    # print("Every ten guesses:")
    # for n in range(0, len(guesses), 10):
    #     print(guesses[n])
    print()
    # Observation: 
    # When teh step size is too small, the convergence happens very slowly. 

    print("f2 with big step size")
    guesses = gradientDescent(func2, dfunc2, np.array([1, 1]), 0.1)
    print("Number of iterations performed:", len(guesses)-1)
    print("Best guess:", guesses[-1])
    print()
    print("Every ten guesses:")
    for n in range(0, len(guesses), 10):
        print(guesses[n])
    print()

    print("f2 with small step size")
    guesses = gradientDescent(func2, dfunc2, np.array([1, 1]), 10**(-7))
    print("Number of iterations performed:", len(guesses)-1)
    print("Best guess:", guesses[-1])
    # print()
    # print("Every ten guesses:")
    # for n in range(0, len(guesses), 10):
    #     print(guesses[n])
    print()
 
    # Observation:
    # Due to the large coefficient on x1, when the step size is about right for x2, x1 diverges (oversteps by a huge amount). However, when 
    # the step size is good for x1, it is too small for x2, so x2 converges very slowly. 


    ### Question 3 ###

    answer = gradientDescent2(funcProb1p2, dfuncProb1p2, np.array([5,5,5]))
    print("Number of iterations performed:", len(answer))
    print(answer[-1])

    # answer = gradientDescent_BT(func1, dfunc1, np.array([5, 5, ]), alpha=1, c1=0.1, rho=0.9)
    # # print(answer)

    