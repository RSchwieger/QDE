def f1(x1, x2, x3, x4):
    return (1-x3)*x2

def f2(x1, x2, x3, x4):
    return x1*(1-x3)*(1-x2)

def f3(x1, x2, x3=0, x4=0):
    return x1*x2

def f4(x1, x2, x3, x4):
    return x2*x1*(1-x3)

def f(x):
    print(x)
    return [f1(*x), f2(*x), f3(*x), f4(*x)]


funcs = {"x1":f1, "x2":f2, "x3":f3, "x4":f3 }

def return_name():
    return "example4"