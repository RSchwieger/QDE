def f1(v1, v2, v3, v4):
    return v2*v3

def f2(v1, v2, v3, v4):
    return 1-v3

def f3(v1, v2, v3, v4):
    return (v1+v2-v1*v2)*v4

def f4(v1, v2, v3, v4):
    return v1*(1-v3)

def f(x):
    return [f1(*x), f2(*x), f3(*x), f4(*x)]

funcs = {"v1":f1, "v2":f2, "v3":f3, "v4": f4}