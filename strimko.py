from constraint import Problem, AllDifferentConstraint, InSetConstraint

grid = """
....
.32.
..1.
....
"""
grid = [list(row.strip()) for row in grid.splitlines() if row.strip()]
S = len(grid)
cellnames = [(i,j) for j, row in enumerate(grid) for i, val in enumerate(row)]
lookup = { (i,j): grid[i][j] for i, j in cellnames }

problem = Problem()
problem.addVariables(cellnames, [str(j) for j in range(1, 5)])

# streams in grid
# [row,column]
problem.addConstraint(AllDifferentConstraint(), [(0, 0), (1, 1), (2, 2), (3, 3)])
problem.addConstraint(AllDifferentConstraint(), [(1, 0), (0, 1), (0, 2), (1, 3)])
problem.addConstraint(AllDifferentConstraint(), [(2, 0), (3, 1), (3, 2), (2, 3)])
problem.addConstraint(AllDifferentConstraint(), [(3, 0), (2, 1), (1, 2), (0, 3)])

for j in range(4):
	# Columns in grid
	problem.addConstraint(AllDifferentConstraint(), [(i, j) for i in range(4)])
	# Rows in grid
	problem.addConstraint(AllDifferentConstraint(), [(j, i) for i in range(4)])


for cell, value in lookup.items():
	if value != ".":
		problem.addConstraint(InSetConstraint([str(value)]), [cell])\

print("\n".join(" ".join(lookup[(i, j)] for j in range(4)) for i in range(4)))


for solution in problem.getSolutions():
	print("\n".join(" ".join(solution[(i, j)] for j in range(4)) for i in range(4)))
	print()

