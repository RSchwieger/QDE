__author__ = 'Robert Schwieger'

from scipy.integrate import ode
import matplotlib.pyplot as plt

# Constants:

k = [2,1,2] # Hill coefficients
theta = [0.5, 0.7, 0.7] # thresholds
d = [1,1.5,0.5] # diagonal of D-Matrix
x0_0 = 1.0;
x0 = [0.3,0.4,0.5] # initial value (1,*,*,*)

# Functions of the ODE-system

def multivariateInterpolation(x):
    """
    Multivariate interpolation
    :param x: list of real numbers in the interval [0,1]
    :return: list of real numbers in the interval [0,1]
    """
    y = [0,0,0]
    """
    y[1] = 1-x[3]
    y[2] = x[1]
    y[3] = x[2]
    """
    y[0] = x0_0*x[2]
    y[1] = (1-x0_0)*x[2]
    y[2] = 1-x[1]


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

# Constants for the ODE-solver

stoppingTime = 20.0
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

# Plot solution

fig, ax = plt.subplots()
ax.set_color_cycle(['green', 'red', 'blue'])
plt.ion()
plt.axis([0.0, stoppingTime, 0.0, 1.1])
for i in range(len(x0)):
    componentOfSolution = [solution[j][i] for j in range(len(solution))] # extract i-th component of solution vector
    plt.plot(evaluationTimes, componentOfSolution, label='x'+str(i+2)) # +2 because the first component was fixed but
    # the names of the variables should remain the same as in application 1

plt.ylabel('x')
plt.xlabel('time')
plt.legend(loc=0)
plt.title("Trajectory of the solutions of the ODE-system with initial state "+str(x0)+", d = "+str(d)+" ,theta = "+str(theta)+", k="+str(k))
plt.show(block=True)

print(multivariateInterpolation(hillCube(x0, k, theta)))

