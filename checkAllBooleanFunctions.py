from pyBoolNetStuff import spit_out_graphs
from BooleanFunctionGenerator import pyBoolNet_Functor_iterator

number_variables = 3

pyBoolNet_bool_funcs = pyBoolNet_Functor_iterator(number_variables)

i = 1
for funcs, variable_name_to_func in pyBoolNet_bool_funcs:
    def f(x):
        return [function(*x) for function in funcs]
    f.list_of_functions = funcs

    difference = spit_out_graphs(variable_to_boolean_function=variable_name_to_func, prefix_of_filename="test_"+str(i),
                    boolean_functions_as_list=f)
    i += 1
    #input = (1, 1)
    #print(variable_name_to_func)
    #print(str(input) + " -> " + str([func(x0=1, x1=1) for func in funcs]))