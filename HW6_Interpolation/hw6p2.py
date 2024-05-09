# hw6p2.py
# CSC 395 Spring 2024
# Name:
# Date:

import numpy as np
import random
import matplotlib.pyplot as plt

"""
noisy_data: creates noisy data centered around the curve defined by func.

INPUTS
func: the function for sampling with noise, func(x).
a, b: the domain [a,b].
N:    the number of data points to generate.
sig:  the standard deviation of the noise.

OUTPUTS
x_vals, y_vals: the x and y values of the noisy data (x in sorted order).
"""
def noisy_data(func, a, b, N, sig):
    # Define random x values in our domain, then sort.
    x_vals = [a+(b-a)*random.random() for ii in range(N)]
    x_vals.sort()

    # Obtain a small additive noise for each data point.
    noise = [np.random.normal(0, sig) for ii in range(N)]

    # Set y = func(x) + noise, and return.
    y_vals = [func(x_vals[ii])+noise[ii] for ii in range(N)]
    return x_vals, y_vals

"""
test_quad: a provided test func for use with noisy_data.
"""
def test_quad(x):
    return (x-2)*(x-3)

"""
TODO: your code goes below!
"""
def poly_fit(x_vals, y_vals, n):
    length = len(x_vals)
    ones = np.ones(length).reshape(-1, 1)
    x_col = np.array(x_vals).reshape(-1, 1)
    y_col = np.array(y_vals).reshape(-1, 1)
    # creating J
    if n < 0:
        raise(Exception)
    elif n == 0: 
        J = ones
    elif n == 1:
        J = np.hstack((ones, x_col))
    else:
        J = np.hstack((ones, x_col))
        for i in range(2, n+1):
            ith_col = np.power(x_col, i)
            J = np.hstack((J, ith_col))

    a = np.transpose(J)@J
    b = np.transpose(J)@y_col
    return np.linalg.solve(a, b)

"""
Python's "main function" block.
"""
if __name__ == "__main__":

    # Set the domain [a,b] and number of points n.
    a = 0
    b = 5
    N = 100

    # Set the order of the polynomial to fit.
    n = 2

    # Set the number of points for plotting and 
    # the std dev of the noise.
    N_lin = 1000
    sig = 0.5

    # Create the noisy data and the linearly spaced x values for
    # plotting.
    (xx,yy) = noisy_data(test_quad, a, b, N, sig)
    x_lin = np.linspace(a, b, N_lin)

    # Call the poly_fit function to perform the fit.
    xi = poly_fit(xx, yy, n)
    print(xi)
    
    # Plot the results and save them.
    plt.scatter(xx, yy)
    ff = [sum([xi[ii]*pow(x,ii) for ii in range(n+1)]) for x in x_lin]
    plt.plot(x_lin, ff)
    plt.show()

'''
Results:
[[ 6.01270012]
 [-4.83695516]
 [ 0.94481248]]
'''
    