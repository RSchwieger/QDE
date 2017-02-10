def f1(x1, x2):
    return 1

def f2(x1, x2):
    return x1

def f(x):
    print(x)
    return [f1(*x), f2(*x)]


funcs = {"x1":f1, "x2":f2 }

def return_name():
    return "example5"