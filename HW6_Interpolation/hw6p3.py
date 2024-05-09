# hw6p3.py
# CSC 395 Spring 2024
# Name:
# Date:

import math
import numpy as np
import matplotlib.pyplot as plt

"""
The test quadratic function for use with fitting.
"""
def test_quad(x):
    return (x-2)*(x-3)

"""
TODO: your implementation goes below!
"""
def lagrange(x, x_vals, y_vals):
    length = len(x_vals)
    Px = 0
    # This loop calculates each term of the polynomial. 
    # A term is the product of the y value of the data point and the corresponding Lagrange basis function
    for i in range(length):
        yi = y_vals[i]
        xi = x_vals[i]
        li = 1
        # This loop calculates the Lagrange basis function for the i-th data point (i.e. l_i(x))
        for j in range(length):
            xj = x_vals[j]
            if j != i:
                li = li * (x-xj)/(xi-xj)

        # Add the term to the polynomial
        Px = Px + yi*li
    return Px

'''
Chebyshev implementation
'''
def chebyshev(a, b, n):
    xx = []
    for k in range(0,n):
        # calculate the Chebyshev nodes
        xk = (a+b)/2 + (b-a)/2*math.cos((2*k+1)*math.pi/(2*n))
        xx.append(xk)
    return xx

"""
Python's "main function" block.
"""
if __name__ == "__main__":

    # Set the domain and number of points.
    a = 0
    b = 5
    n = 80

    # Set the number of points for plotting, the plotting x values,
    # and the plot window.
    n_plot = 1000
    x_plot = np.linspace(a,b,n_plot)
    window = [a,b,-4,10] # specific for test_quad.
    
    # Create linearly spaced x values and sample the test function.
    x_lin = np.linspace(a,b,n)
    y_lin = np.array([test_quad(x) for x in x_lin])

    # Obtain the y values from the Lagrange Polynomial Interpolation.
    l_plot = [lagrange(x, x_lin, y_lin) for x in x_plot]

    # Plot the original data and the interpolated polynomial.
    plt.scatter(x_lin, y_lin)
    plt.plot(x_plot, l_plot)
    plt.axis(window)
    plt.show()

    # Now define the Chebyshev nodes. TODO: you will need to update this!
    x_cheb = chebyshev(a,b,n) #FIXME!
    y_cheb = np.array([test_quad(x) for x in x_cheb])

    # print(x_cheb)
    # print(y_cheb)

    # Obtain the y values from the Lagrange Polynomial Interpolation.
    l_cheb = [lagrange(x, x_cheb, y_cheb) for x in x_plot]

    # Plot the original data and the interpolated polynomial.
    plt.scatter(x_cheb, y_cheb)
    plt.plot(x_plot, l_cheb)
    plt.axis(window)
    plt.show()
