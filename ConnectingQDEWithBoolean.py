from itertools import product
from sign_algebra import *
from proposition2 import *

def example_f(x):
    return [1-x[2], x[0], x[1], x[0]*x[2]]

def phi(x, f):
    """
    Constructs the time derivative of a boolean function f
    :param x: state in {0,1}^N
    :param f: function {0,1}^N -> {0,1}^N
    :return: \dot x
    """
    y = f(x)
    ret = [y[i] - x[i] for i in range(len(x))]

    return [phi.value_to_sign[x] for x in ret]
phi.value_to_sign = {1: p, -1: m, 0: n}

def alternative_phi(x, f):
    y = f(x)
    ret = [y[i] - x[i] for i in range(len(x))]
    rret = []
    for i in range(len(ret)):
        if ret[i] != 0:
            rret += [ alternative_phi.value_to_sign[ret[i]] ]
        else:
            temp = (-1)**(1-x[i])
            rret += [ alternative_phi.value_to_sign[temp] ]
    return rret
alternative_phi.value_to_sign = {1: p, -1: m}

if __name__ == "__main__":
    x_0 = [0, 1, 0, 1]

    for state in product([0, 1], repeat=len(x_0)):
        print(str(state) + " --> " +str(tuple(phi(state, example_f))))

    #print(phi(x_0, example_f))