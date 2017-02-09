from sign_algebra import *
from proposition2 import *

"""
In this file several examples from the cytokinin project are depicted. The components are depicted in the following way
P B A Ap. We additionaly attach to each component a negative loop due to a decay rate in the ODE-model.
"""


# 1) Model A

"""
-0-0
+-00
0+-0
+0+-
"""

sign_matrix_1 = [[n]*4 for i in range(4)]

sign_matrix_1[0][2] = m
sign_matrix_1[0][0] = m

sign_matrix_1[1][0] = p
sign_matrix_1[1][1] = m

sign_matrix_1[2][1] = p
sign_matrix_1[2][2] = m

sign_matrix_1[3][0] = p
sign_matrix_1[3][2] = p
sign_matrix_1[3][3] = m

# 2) Model AB

"""
---0
+-00
0+-0
+0+-
"""
sign_matrix_2 = [[n]*4 for i in range(4)]

sign_matrix_2[0][1] = m
sign_matrix_2[0][2] = m

sign_matrix_2[1][0] = p

sign_matrix_2[2][1] = p

sign_matrix_2[3][0] = p
sign_matrix_2[3][2] = p

# + diagonal elements
sign_matrix_2[0][0] = m
sign_matrix_2[1][1] = m
sign_matrix_2[2][2] = m
sign_matrix_2[3][3] = m

# 3) Model B

"""
-000
+-0+
0+-0
+0+-
"""
sign_matrix_3 = [[n]*4 for i in range(4)]

sign_matrix_3[1][0] = p
sign_matrix_3[1][3] = p

sign_matrix_3[2][1] = p

sign_matrix_3[3][0] = p
sign_matrix_3[3][2] = p

# + diagonal elements
sign_matrix_3[0][0] = m
sign_matrix_3[1][1] = m
sign_matrix_3[2][2] = m
sign_matrix_3[3][3] = m

#---------------------------------------------------------------------------------------------------------------------

# 3) Model P

"""
-000
+-0+
0+-0
+0+-
"""
sign_matrix_4 = [[n]*4 for i in range(4)]

sign_matrix_4[0][3] = m

sign_matrix_4[1][0] = p

sign_matrix_4[2][1] = p

sign_matrix_4[3][0] = p
sign_matrix_4[3][2] = p

# + diagonal elements
sign_matrix_4[0][0] = m
sign_matrix_4[1][1] = m
sign_matrix_4[2][2] = m
sign_matrix_4[3][3] = m

#---------------------------------------------------------------------------------------------------------------------

"""
Now we construct the edge set of the abstractions of the QDE
"""

def getDiff(list1, list2):
    """
    Returns list1-list2
    :param list1:
    :param list2:
    :return:
    """
    return [item for item in list1 if item not in list2]

def symmetricDiff(list1, list2):
    return getDiff(list1, list2)+getDiff(list2, list1)

def getEdgesAsLatexTable(edges):
    """
    \begin{center}
  \begin{tabular}{ l | c | r }
    \hline
    1 & 2 & 3 \\ \hline
    4 & 5 & 6 \\ \hline
    7 & 8 & 9 \\
    \hline
  \end{tabular}
\end{center}
    """
    string = "\\begin{tabular}{ l | r }\n"
    string += " \\hline\n"
    for edge in diff_AB_A:
        string += " " + str(edge[0]) + " & " + str(edge[1]) + " \\\\" + "  \\hline"+ "\n"
    string += " \\hline\n"
    string += "\\end{tabular}"
    return string

edgesA = get_edges(sign_matrix_1)
edgesAB = get_edges(sign_matrix_2)
edgesB = get_edges(sign_matrix_3)
edgesP = get_edges(sign_matrix_4)

# We are interested in the differences between the models
diff_AB_A = getDiff(edgesAB, edgesA)
diff_A_AB = getDiff(edgesA, edgesAB)
diff_B_AB = getDiff(edgesB, edgesAB)
diff_AB_B = getDiff(edgesAB, edgesB)
diff_P_B = getDiff(edgesP, edgesB)
diff_B_P = getDiff(edgesB, edgesP)
diff_AB_P = getDiff(edgesAB, edgesP)
diff_P_AB = getDiff(edgesP, edgesAB)

file = open('table.txt', 'w')


print("Edges from Model AB / Model A:\n")

file.write("E(A) triangle E(AB):\n\n")
file.write(getEdgesAsLatexTable(symmetricDiff(edgesAB, edgesA)))
file.write("\n\n"+5*"--------"+"\n")

file.write("E(A) triangle E(B):\n\n")
file.write(getEdgesAsLatexTable(symmetricDiff(edgesA, edgesB)))
file.write("\n\n"+5*"--------"+"\n")

file.write("E(A) triangle E(P):\n\n")
file.write(getEdgesAsLatexTable(symmetricDiff(edgesA, edgesP)))
file.write("\n\n"+5*"--------"+"\n")

file.write("E(AB) triangle E(B):\n\n")
file.write(getEdgesAsLatexTable(symmetricDiff(edgesAB, edgesB)))
file.write("\n\n"+5*"--------"+"\n")

file.write("E(AB) triangle E(P):\n\n")
file.write(getEdgesAsLatexTable(symmetricDiff(edgesAB, edgesP)))
file.write("\n\n"+5*"--------"+"\n")

file.write("E(B) triangle E(P):\n\n")
file.write(getEdgesAsLatexTable(symmetricDiff(edgesB, edgesP)))
file.write("\n\n"+5*"--------"+"\n")


print("\nEdges from Model A / Model AB:\n")
for edge in diff_A_AB:
    print(edge)

print("\nE(A) triangle E(AB):\n")
for edge in symmetricDiff(edgesA, edgesAB):
    print(edge)

"""
print("\nEdges from Model B / Model AB:\n")
for edge in diff_B_AB:
    print(edge)

print("\nEdges from Model AB / Model B:\n")
for edge in diff_AB_B:
    print(edge)

print("\nEdges from Model B / Model P:\n")
for edge in diff_B_P:
    print(edge)

print("\nEdges from Model P / Model B:\n")
for edge in diff_P_B:
    print(edge)

print("\nEdges from Model AB / Model P:\n")
for edge in diff_AB_P:
    print(edge)

print("\nEdges from Model P / Model AB:\n")
for edge in diff_P_AB:
    print(edge)
"""