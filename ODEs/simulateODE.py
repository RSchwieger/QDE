from scipy.integrate import ode
import matplotlib.pyplot as plt
from sign_algebra import *
from ODEs import runningExample as application

f = application.f
x0 = application.x0
theta = application.theta
d = application.d
k  = application.k

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

def abstract_solution(solution, dt):
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
    t = 0
    last_element = (sequence[0], t)
    abstraction = [last_element]
    for elem in sequence[1:]:
        t += dt
        if elem != last_element[0]:
            last_element = (elem, t)
            abstraction += [(elem, round(t,3))]
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
print(abstract_solution(get_derivatives(solution), dt))

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
