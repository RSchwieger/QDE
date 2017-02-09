__author__ = 'Robert Schwieger'

from scipy.integrate import ode
import matplotlib.pyplot as plt
from sign_algebra import *

# Constants:

k = [4,4,4] # Hill coefficients
theta = [0.5, 0.5, 0.5] # thresholds
d = [1,1,1] # diagonal of D-Matrix
x0 = [0.85,0.25,0.85] # initial value (1,*,*)

# Functions of the ODE-system

def multivariateInterpolation(x):
    """
    Multivariate interpolation
    :param x: list of real numbers in the interval [0,1]
    :return: list of real numbers in the interval [0,1]
    """
    y = [0,0,0]
    y[0] = (1-x[2])+x[1]-(1-x[2])*x[1] #(1-x3)+x2-(1-x3)*x2
    y[1] = x[0]*(1-x[1])
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

def get_derivatives(solutions):
    """
    Returns the derivative of a time series [(,,,,),...]
    :param solutions: [(,,,,),...]
    :return: derivative
    """
    return [f(0, solution) for solution in solutions]

def convert_vector_in_sign_vector(vec):
    """
    Converts a vector like [0.23, -0.1] to [+,-]
    :param vec:
    :return:
    """
    ret = []
    for x in vec:
        if x<0:
            ret += [m]
        elif x>0:
            ret += [p]
        else:
            ret += [n]
    return ret

def abstract_solution(solution):
    """
    Computes the abstraction of a solution according to the QDE theory.
    1) Compute a sequence of signs
    2 ) delete repetitions
    :param solution:
    :return:
    """
    sequence = [convert_vector_in_sign_vector(vec) for vec in solution]
    if len(sequence) == 0:
        return sequence
    last_element = sequence[0]
    abstraction = [last_element]
    for elem in sequence[1:]:
        if elem != last_element:
            last_element = elem
            abstraction += [elem]
    return abstraction


# Constants for the ODE-solver

stoppingTime = 10.0
number_of_steps = 10**4 # Anzahl der Iterationen
dt = stoppingTime/number_of_steps # Schrittgröße

# Solving the ODE-system

y = ode(f).set_integrator('dopri5')
y.set_initial_value(x0, 0.0) # set initial value at time = 0
evaluationTimes = [0.0] # initialized
solution = [x0] # save the first time step

while y.successful() and y.t < stoppingTime:
    evaluationTimes += [y.t+dt]
    y.integrate(y.t+dt)
    solution += [list(y.y)]

    if y.successful() is False:
        print("Something went wrong during r.integrate()")

# Abstraction

print("The abstraction of the solution is: \n")
print(abstract_solution(get_derivatives(solution)))

# Plot solution

plt.ion()
plt.axis([0.0, stoppingTime, 0.0, 1.1])
for i in range(len(x0)):
    componentOfSolution = [solution[j][i] for j in range(len(solution))] # extract i-th component of solution vector
    plt.plot(evaluationTimes, componentOfSolution, label='x'+str(i+1))

plt.ylabel('x')
plt.xlabel('time')
plt.legend(loc=0)
plt.title("Trajectory of the solutions of the ODE-system with initial state "+str(x0)+", d = "+str(d)+" ,theta = "+str(theta)+", k="+str(k))
plt.show(block=True)

