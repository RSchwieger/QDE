def f1(x1, x2, x3):
    return (1-x3)+x2-(1-x3)*x2

def f2(x1, x2, x3):
    return x1*(1-x2)

def f3(x1, x2, x3):
    return x2

def f(x):
    return [f1(*x), f2(*x), f3(*x)]

funcs = {"x1":f1, "x2":f2, "x3":f3 }

def return_name():
    return "example3"