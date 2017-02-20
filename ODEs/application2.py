__author__ = 'Robert Schwieger'

from scipy.integrate import ode
import matplotlib.pyplot as plt
from sign_algebra import *

# Constants:

k = [12,11,12] # Hill coefficients
theta = [0.4, 0.5, 0.5] # thresholds
d = [1,1,1] # diagonal of D-Matrix
x0 = [0.75,0.85,0.75] # initial value (1,*,*)

# Functions of the ODE-system

def multivariateInterpolation(x):
    """
    Multivariate interpolation
    :param x: list of real numbers in the interval [0,1]
    :return: list of real numbers in the interval [0,1]
    """
    y = [0,0,0]
    y[0] = (1-x[2])+x[1]-(1-x[2])*x[1] #(1-x3)+x2-(1-x3)*x2
    y[1] = x[0]*(1-x[2])
    y[2] = x[1]
    return y

def hillCube(x, k, theta):
    """
    Computes the Hill Cube at x with Hill coefficients k and threshold theta
    :param x: list of input values of the Hill Cube of length N
    :param k: list of Hill coefficients of length N
    :param theta: list of thresholds of length N
    :return: result of the Hill Cube evaluated at x represented as a list of length N
    """
    return [(x[i]**k[i])/(x[i]**k[i]+theta[i]**k[i]) for i in range(len(x))]

def f(t,x):
    """
    Function of the ODE-system written in the form required by the ODE-solver
    :param t: Not used
    :param x: list of input values
    :return: function evaluation saves as list
    """
    discreteTimestep = multivariateInterpolation(hillCube(x, k, theta))
    return [d[i]*(discreteTimestep[i]-x[i]) for i in range(len(discreteTimestep))]

# Some functions to determine the abstraction of the solution (QDE theory)