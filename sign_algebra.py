__author__ = 'robert'

from itertools import product

NULL = 0
PLUS = 1
MINUS = -1
Q = 100

class Signum:
    def __init__(self, sign):
        self.sign = sign

    def __str__(self):
        if self.sign == NULL:
            return "0"
        if self.sign == PLUS:
            return "+"
        if self.sign == MINUS:
            return "-"
        if self.sign == Q:
            return "?"
        else:
            return "Unknown value"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if self.sign == PLUS and other.sign == PLUS:
            return Signum(PLUS)
        if self.sign == PLUS and other.sign == NULL:
            return Signum(PLUS)
        if self.sign == PLUS and other.sign == MINUS:
            return Signum(Q)
        if self.sign == PLUS and other.sign == Q:
            return Signum(Q)

        if self.sign == NULL and other.sign == PLUS:
            return Signum(PLUS)
        if self.sign == NULL and other.sign == NULL:
            return Signum(NULL)
        if self.sign == NULL and other.sign == MINUS:
            return Signum(MINUS)
        if self.sign == NULL and other.sign == Q:
            return Signum(Q)

        if self.sign == MINUS and other.sign == PLUS:
            return Signum(Q)
        if self.sign == MINUS and other.sign == NULL:
            return Signum(MINUS)
        if self.sign == MINUS and other.sign == MINUS:
            return Signum(MINUS)
        if self.sign == MINUS and other.sign == Q:
            return Signum(Q)

        if self.sign == Q and other.sign == PLUS:
            return Signum(Q)
        if self.sign == Q and other.sign == NULL:
            return Signum(Q)
        if self.sign == Q and other.sign == MINUS:
            return Signum(Q)
        if self.sign == Q and other.sign == Q:
            return Signum(Q)

    def __mul__(self, other):
        if self.sign == PLUS and other.sign == PLUS:
            return Signum(PLUS)
        if self.sign == PLUS and other.sign == NULL:
            return Signum(NULL)
        if self.sign == PLUS and other.sign == MINUS:
            return Signum(MINUS)
        if self.sign == PLUS and other.sign == Q:
            return Signum(Q)

        if self.sign == NULL and other.sign == PLUS:
            return Signum(NULL)
        if self.sign == NULL and other.sign == NULL:
            return Signum(NULL)
        if self.sign == NULL and other.sign == MINUS:
            return Signum(NULL)
        if self.sign == NULL and other.sign == Q:
            return Signum(NULL)

        if self.sign == MINUS and other.sign == PLUS:
            return Signum(MINUS)
        if self.sign == MINUS and other.sign == NULL:
            return Signum(NULL)
        if self.sign == MINUS and other.sign == MINUS:
            return Signum(PLUS)
        if self.sign == MINUS and other.sign == Q:
            return Signum(Q)

        if self.sign == Q and other.sign == PLUS:
            return Signum(Q)
        if self.sign == Q and other.sign == NULL:
            return Signum(NULL)
        if self.sign == Q and other.sign == MINUS:
            return Signum(Q)
        if self.sign == Q and other.sign == Q:
            return Signum(Q)#

    def __eq__(self, other):
        if self.sign == PLUS and other.sign == PLUS:
            return True
        if self.sign == PLUS and other.sign == NULL:
            return False
        if self.sign == PLUS and other.sign == MINUS:
            return False
        if self.sign == PLUS and other.sign == Q:
            return True

        if self.sign == NULL and other.sign == PLUS:
            return False
        if self.sign == NULL and other.sign == NULL:
            return True
        if self.sign == NULL and other.sign == MINUS:
            return False
        if self.sign == NULL and other.sign == Q:
            return True

        if self.sign == MINUS and other.sign == PLUS:
            return False
        if self.sign == MINUS and other.sign == NULL:
            return False
        if self.sign == MINUS and other.sign == MINUS:
            return True
        if self.sign == MINUS and other.sign == Q:
            return True

        if self.sign == Q and other.sign == PLUS:
            return True
        if self.sign == Q and other.sign == NULL:
            return True
        if self.sign == Q and other.sign == MINUS:
            return True
        if self.sign == Q and other.sign == Q:
            return True

p = Signum(PLUS)
n = Signum(NULL)
m = Signum(MINUS)
q = Signum(Q)


class Vector:
    def __init__(self, list_of_values):
        self.list_of_values = list_of_values

    def __str__(self):
        return str(self.list_of_values)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return Vector([self[i]+other[i] for i in range(len(self))])
    def __eq__(self, other):
        for i in range(len(self.list_of_values)):
            if self.list_of_values[i] != other.list_of_values[i]:
                return False
        return True

    def __len__(self):
        return len(self.list_of_values)

    def __getitem__(self, index):
        return self.list_of_values[index]

    def support(self):
        return [i for i in range(len(self)) if self[i].sign != NULL]

    def support_complement(self):
        return [i for i in range(len(self)) if self[i].sign == NULL]

    def wedge(self, other):
        return Vector([self[i] if self[i].sign == other[i].sign else Signum(NULL) for i in range(len(self))])


if __name__ == "__main__":
    iter = product([NULL, PLUS, MINUS, Q], repeat=2)
    print(type(iter))
    for i in iter:
        print(i)