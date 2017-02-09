from PyBoolNet import InteractionGraphs as IGs
from PyBoolNet import QuineMcCluskey as QMC
from PyBoolNet import StateTransitionGraphs as STGs

from ConnectingQDEWithBoolean import alternative_phi as phi
from Examples import example5 as example
from proposition2 import is_there_an_edge_between
from sign_algebra import *
from copy import deepcopy

example_filename = example.return_name()

def binary_string_to_components(binary_string):
    """
    Converts smth. like '10011' into [1,0,0,1,1]
    :param binary_string:
    :return: list of elements in {0,1}
    """
    return [int(x) for x in binary_string]

def function_is_monotonous(interaction_graph):
    """
    Returns true if the interaction graph stems from a monontonous function,
    :param interaction_graph:
    :return:
    """
    for edge in interaction_graph.edges(data=True): # data=True gives us also the signs of the edges
        print(edge)
        if len(edge[2]['sign']) > 1:
            return False
    return True

def graph_to_adj_matrix(interaction_graph):
    """
    Converts the interaction graph into a sign matrix with elements from the sign algebra
    :param interaction_graph:
    :return: adjacency matrix of the interaction graph, nodes, nodes_to_number
    """
    nodes = interaction_graph.nodes() # list number to node
    nodes.sort()
    nodes_to_number = dict([(nodes[i], i) for i in range(len(nodes))]) # dictionary node -> number
    sign_dict = {1: p, 0: n, -1: m} # signs

    # initialize adjacency matrix with zeros everywhere
    sign_matrix = [[n] * len(nodes) for i in range(len(nodes))]

    for edge in interaction_graph.edges(data=True):
        #print(edge)
        v1 = nodes_to_number[edge[0]]
        v2 = nodes_to_number[edge[1]]
        sign = edge[2]['sign']
        sign_matrix[v2][v1] = sign_dict[list(sign)[0]] # the set sign has only one element
        #print(str((v1,v2))+" -> "+str(sign_matrix[v2][v1]))

    return sign_matrix, nodes, nodes_to_number

def deleteEdgesWithQdE(state_transition_graph, sign_matrix, boolean_functions_as_list):
    """
    Return a modified state transition graph which contains only edges which are compatible with the stg of the QDE.
    :param state_transition_graph:
    :param sign_matrix:
    :return:
    """
    # Iterate through all edges of the derived graph
    state_transition_graph = deepcopy(state_transition_graph)
    edge_deleted = False
    for edge in state_transition_graph.edges():
        conv_edge = (binary_string_to_components(edge[0]), binary_string_to_components(edge[1]))
        derivated_edge = (phi(conv_edge[0], f=boolean_functions_as_list), phi(conv_edge[1], f=boolean_functions_as_list))
        transition_compatible_with_QDE = \
            is_there_an_edge_between(v=Vector(derivated_edge[0]), w=Vector(derivated_edge[1]), sigma=sign_matrix)
        transition_compatible_with_QDE = transition_compatible_with_QDE or (derivated_edge[0] == derivated_edge[1])
        if not transition_compatible_with_QDE:
            state_transition_graph.remove_edge(*edge)
            edge_deleted = True
        print(str(edge) + " becomes " + str(derivated_edge)
              +" and is compatible with QDE = "+str(transition_compatible_with_QDE))
    return state_transition_graph, edge_deleted

def substract_identity(interaction_graph):
    dim = len(interaction_graph)
    for i in range(dim):
        interaction_graph[i][i] = interaction_graph[i][i]+m
    return interaction_graph

def interaction_graph_has_self_loops(interaction_graph):
    sign_matrix, nodes, nodes_to_number = graph_to_adj_matrix(interaction_graph)
    for i in range(len(nodes)):
        if sign_matrix[i][i] != n:
            return True
    return False

def spit_out_graphs(variable_to_boolean_function, prefix_of_filename, boolean_functions_as_list,
                    show_only_if_difference_between_stg_and_reduced_stg = False):
    prime_implicants = QMC.functions2primes(variable_to_boolean_function)

    # Create the interaction graph
    igraph = IGs.primes2igraph(prime_implicants)

    graph_to_adj_matrix(igraph)

    if not function_is_monotonous(interaction_graph=igraph):
        print("Error: This function is not monotonous.")
        return
    else:
        pass
        #print("The function is monotonous.")

    # Only consider interaction graphs wihtout self loops
    #if interaction_graph_has_self_loops(igraph):
        #print("Skip this graph since it has a self loop.")
    #    return
    #else:
    #    print("Interacion graph has no self loops")

    # Construct the state transition graph
    state_transition_graph = STGs.primes2stg(prime_implicants, "asynchronous")

    # Convert the igraph into an adajacency matrix
    sign_matrix, number_to_nodes, nodes_to_number = graph_to_adj_matrix(igraph)
    #print("The sign_matrix of f is:\n"+str(sign_matrix))
    #print("number to nodes are \n" + str(number_to_nodes))
    #print("nodes to number are \n"+str(nodes_to_number))

    sign_matrix = substract_identity(sign_matrix) # We want the sign matrix of f-id
    #print("The sign_matrix of f-id is:\n"+str(sign_matrix))
    reduced_state_transition_graph, edge_deleted = deleteEdgesWithQdE(state_transition_graph, sign_matrix,
                                                                      boolean_functions_as_list)
    if show_only_if_difference_between_stg_and_reduced_stg:
        if edge_deleted:
            STGs.stg2image(state_transition_graph, prefix_of_filename + "_stg.png")
            STGs.stg2image(reduced_state_transition_graph, prefix_of_filename + "_stg_smaller.png")
            IGs.create_image(prime_implicants, prefix_of_filename + "_igraph.png")
    else:
        STGs.stg2image(state_transition_graph, prefix_of_filename + "_stg.png")
        STGs.stg2image(reduced_state_transition_graph, prefix_of_filename+"_stg_smaller.png")
        IGs.create_image(prime_implicants, prefix_of_filename+"_igraph.png")

    return edge_deleted



if __name__ == "__main__":
    spit_out_graphs(variable_to_boolean_function=example.funcs, prefix_of_filename=example_filename,
                    boolean_functions_as_list=example.f)