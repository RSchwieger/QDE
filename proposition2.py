__author__ = 'robert'

from sign_algebra import *
from itertools import product

def is_there_an_edge_between(v, w, sigma):
    """
    Tests whether there is an edge in the state transition graph of an QDE with sign matrix
    sigma between v and w with Prop. 2
    :param v: first vertex of the edge
    :param w: second vertex of the edge
    :param sigma: sign matrix
    :return: True for yes, False for no
    """
    x = v.wedge(w) # find out which components change
    for i in x.support_complement():
        #print(i)
        for j in x.support(): # iterate over all components of v which don't change during the transition v -> w
            if w[i]*x[j] == sigma[i][j]:
                return True
        return False

def get_edges(sign_matrix):
    edges = []
    length = len(sign_matrix)
    for lv in product([p, m], repeat=length):
        for lw in product([p, m], repeat=length):
            v = Vector(lv)
            w = Vector(lw)
            if v != w and is_there_an_edge_between(v, w, sign_matrix):
                edges += [(v,w)]
    return edges
