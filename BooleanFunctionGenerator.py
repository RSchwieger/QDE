from itertools import product

number_variables = 2


class boolean_function_iterator:
    """
    This class defines an iterator which iterates over all boolean functions. {0,1}**number_variables -> {0,1}.
    The functions are represented as dictionaries {0,1}**number_variables -> {0,1}
    """
    def __init__(self, number_variables):
        self.number_variables = number_variables

        self.input_states = []
        # Iterate over all input states
        for input_state in product([0, 1], repeat=number_variables):
            self.input_states += [input_state]

        self.output_state_iterator = iter(product([0, 1], repeat=len(self.input_states)))

        # Stores the current function
        self.current_function_dictionary = {}


    def __iter__(self):
        output_state = next(self.output_state_iterator)

        for i in range(len(output_state)):
            self.current_function_dictionary[self.input_states[i]] = output_state[i]

        return self

    def __next__(self):
        try:
            output_state = next(self.output_state_iterator)
            for i in range(len(output_state)):
                self.current_function_dictionary[self.input_states[i]] = output_state[i]
            result = self.current_function_dictionary
            return dict(result)
        except StopIteration:
            raise(StopIteration)


class boolean_Functor_iterator:
    """
    This class implements an iterator over all boolean functions {0,1}**number_variables -> {0,1}**number_variables

    it returns a list of functions of the format

    def boolean_function(x):
        ...
        return something in {0,1}

    and x is a list
    """
    def __init__(self, number_variables):
        self.number_variables = number_variables

        bool_funcs_to_1d = boolean_function_iterator(number_variables)
        self.functor_iterator = product(bool_funcs_to_1d, repeat=number_variables)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            current_func_dicts = next( self.functor_iterator)
            result = []
            for i in range(len(current_func_dicts)):
                def boolean_function(x):
                    return boolean_function.func_dict[x]
                boolean_function.func_dict = current_func_dicts[i]
                result += [boolean_function]
            return result
        except StopIteration:
            raise(StopIteration)

def get_variable_names(input_length):
    """
    Depending on the input length it generates a list of variable names
    :param input_length:
    :return:
    """
    return ["x"+str(i) for i in range(input_length)]

def func_to_pyBoolNet_format(function,input_length):
    """
    Converts a function which takes the parameters as a list
    into a function with parameters x0, x1, x2, ...
    :param function:
    :param input_length:
    :return:
    """
    variable_names = get_variable_names(input_length)
    arguments_str = ""
    for var in variable_names:
        arguments_str += var+", "
    arguments_str = arguments_str[:-2]

    namespace = {}
    namespace['function'] = function
    function_head = "def wrapper("+arguments_str+"):"
    function_code = """
    parameter_dict = locals()
    parameters = list(parameter_dict.keys())
    args = [parameter_dict[param] for param in parameters]
    return function(tuple(args))
    """
    code_block = function_head+function_code
    exec(code_block, namespace)
    #function(tuple([0,1]))
    return namespace['wrapper']

class pyBoolNet_Functor_iterator:
    """
    A wrapper for boolean_Functor_iterator. The returned functions now have the form

    def boolean_function(x0, x1, ..., x(number_variables-1)):
        ...
        return something in {0,1}

    This is necessary due to compatibility reasons with pyBoolNet
    """
    def __init__(self, number_variables):
        self.number_variables = number_variables
        self.bool_func_iterator = boolean_Functor_iterator(number_variables)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            current_funcs = next(self.bool_func_iterator)
            list_of_functions = [func_to_pyBoolNet_format(func, self.number_variables) for func in current_funcs]

            variable_name_to_func = {}
            variable_names = get_variable_names(self.number_variables)
            for variable_name, function in zip(variable_names, list_of_functions):
                variable_name_to_func[variable_name] = function
            return list_of_functions, variable_name_to_func
        except StopIteration:
            raise(StopIteration)


if __name__ == "__main__":
    bool_funcs_to_1d = boolean_function_iterator(number_variables)
    bool_funcs = boolean_Functor_iterator(number_variables)
    pyBoolNet_bool_funcs = pyBoolNet_Functor_iterator(number_variables)

    for funcs, variable_name_to_func in pyBoolNet_bool_funcs:
        input = (1,1)
        print(variable_name_to_func)
        print(str(input)+" -> "+str([func(x0=1, x1=1) for func in funcs]))

