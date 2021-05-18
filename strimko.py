from typing import List, Any, Tuple

from constraint import Problem, AllDifferentConstraint, InSetConstraint
import re

size = int(input('podaj wielkosc lamiglowki: '))

res = [["." for i in range(size)] for j in range(size)]

for r in res:
    for c in r:
        print(c, end=" ")
    print()

S = len(res)
problem = Problem()

for j in range(size):
    array: List[Tuple[Any, Any]] = []
    x = []
    route = input('podaj sciezke nr ' + str(j) + ' [rzad, kolumna]: \n')
    x = re.findall("[0-9]+", route)
    print(x)
    for i in range(0, len(x), 2):
        print(i)
        array.append((int(x[i]), int(x[i + 1])))
        print(array)
    problem.addConstraint(AllDifferentConstraint(), array)

for i in range(size - 1):
    values = input('uzupelnij wybrane miejsce: \n')
    x = re.findall("[0-9]+", values)
    res[int(x[0])][int(x[1])] = x[2]

cellnames = [(i, j) for j, row in enumerate(res) for i, val in enumerate(row)]
lookup = {(i, j): res[i][j] for i, j in cellnames}
problem.addVariables(cellnames, [str(j) for j in range(1, size + 1)])

# streams in grid
# [row,column]
# problem.addConstraint(AllDifferentConstraint(), [(0, 0), (1, 1), (2, 2), (3, 3)])
# problem.addConstraint(AllDifferentConstraint(), [(1, 0), (0, 1), (0, 2), (1, 3)])
# problem.addConstraint(AllDifferentConstraint(), [(2, 0), (3, 1), (3, 2), (2, 3)])
# problem.addConstraint(AllDifferentConstraint(), [(3, 0), (2, 1), (1, 2), (0, 3)])

for j in range(size):
    # Columns in grid
    problem.addConstraint(AllDifferentConstraint(), [(i, j) for i in range(size)])
    # Rows in grid
    problem.addConstraint(AllDifferentConstraint(), [(j, i) for i in range(size)])

for cell, value in lookup.items():
    if value != ".":
        problem.addConstraint(InSetConstraint([str(value)]), [cell])
        print("check")
print("\n".join(" ".join(lookup[(i, j)] for j in range(size)) for i in range(size)))

for solution in problem.getSolutions():
    print("\n".join(" ".join(solution[(i, j)] for j in range(size)) for i in range(size)))
    print()
