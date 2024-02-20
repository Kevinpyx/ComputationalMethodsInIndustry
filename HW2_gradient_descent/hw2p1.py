import numpy as np

def func(x): # takes in a 2D numpy array
    return x[0]**2 + x[1]**2

def dfunc(x): # takes in a 2D numpy array
    return np.array([2*x[0], 2*x[1]])


def gradientDescent (func, dfunc, x0, alpha, iternum=100, tol=10**(-6)):
    # fx = func(x0)
    gradf = dfunc(x0)
    norm = np.linalg.norm(gradf)
    lst = [x0]

    while iternum>0 and norm>tol:
        # calculate new x and append to the list 
        x1 = x0 - alpha*gradf 
        lst.append(x1)

        # update x and calculate new grad
        x0 = x1
        gradf = dfunc(x0)
        norm = np.linalg.norm(gradf)

        # update iternum
        iternum -= 1 

    return lst

# unfinished
# 
def gradientDescent_BT (func, dfunc, x0, alpha, iternum=100, tol=10**(-6)):
    # fx = func(x0)
    gradf = dfunc(x0)
    norm = np.linalg.norm(gradf)

    while iternum>0 and norm>tol:
        # calculate new x and append to the list 
        x1 = x0 - alpha*gradf 

        # update x and calculate new grad
        x0 = x1
        gradf = dfunc(x0)
        norm = np.linalg.norm(gradf)

        # update iternum
        iternum -= 1 

    return x1


"""
Main
"""
if __name__ == "__main__":
    answer = gradientDescent(func, dfunc, np.array([5, 5]), 0.1)
    # print(answer)
    print("Number of iterations performed:", len(answer))
    print("Function values: ")
    for x in answer:
        print(func(x))