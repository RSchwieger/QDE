def f1(x1, x2, x3, x4):
    return x1+x2-x1*x2

def f2(x1, x2, x3, x4):
    return x1*x4

def f3(x1, x2, x3, x4):
    return x2*(1-x4)

def f4(x1, x2, x3, x4):
    return 1-x3

def f(x):
    print(x)
    return [f1(*x), f2(*x), f3(*x), f4(*x)]


funcs = {"x1":f1, "x2":f2, "x3":f3, "x4":f4}

def return_name():
    return "example7"