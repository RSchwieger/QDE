__author__ = 'robert'

from sign_algebra import *
from itertools import product

import networkx as nx
import matplotlib.pyplot as plt

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
    """
    Returns a list of edges
    :param sign_matrix:
    :return:
    """
    edges = []
    length = len(sign_matrix)
    for lv in product([p, m], repeat=length):
        for lw in product([p, m], repeat=length):
            v = Vector(lv)
            w = Vector(lw)
            if v != w and is_there_an_edge_between(v, w, sign_matrix):
                edges += [(v,w)]
    return edges

def convert_edge(edge):
    sign_dict = {str(m): 0, str(p):1}
    vertex1 = [sign_dict[str(s)] for s in edge[0]]
    vertex2 = [sign_dict[str(s)] for s in edge[1]]
    return (vertex1, vertex2)

def construct_qde_graph(sign_matrix, zero_one_representation=True):
    """
    Constructs a QDE-graph
    :param sign_matrix:
    :return:
    """
    qde_graph = nx.DiGraph()
    edges = get_edges(sign_matrix)
    for edge in edges:
        if zero_one_representation:
            edge = convert_edge(edge)
        qde_graph.add_edge(str(edge[0]), str(edge[1]))
    return qde_graph

def save_plot_of_qde_graph(qde_graph, filename):
    #nx.draw(qde_grap, with_labels=True)
    node_labels = {node: node for node in qde_graph.nodes()}
    nx.draw(qde_graph, pos=nx.spring_layout(qde_graph), node_size=2500, with_labels=True)
    nx.drawing.nx_pydot.write_dot(qde_graph, filename.replace(".png", ".dot"))
    #nx.write_dot(qde_graph, filename+'.dot')
    #nx.draw_networkx_labels(qde_graph, pos=nx.spring_layout(qde_graph), labels=node_labels)
    plt.draw()
    plt.savefig(filename)
    plt.close()

def create_scc_graph(graph):
    sccs = nx.strongly_connected_components(graph)
    condensation = nx.condensation(graph, sccs)
    return condensation, condensation.graph['mapping']


if __name__ == "__main__":
    sign_matrix = [[n, p, m], [m, n, m], [m, n, n]]
    qde_graph = construct_qde_graph(sign_matrix)
    scc_graph = create_scc_graph(qde_graph)
    save_plot_of_qde_graph(qde_graph, "test.png")
    save_plot_of_qde_graph(scc_graph, "test2.png")
