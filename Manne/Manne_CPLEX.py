from docplex.mp.model import Model

# Define the number of tasks and machines
n = 4

# Define a large constant
P = 10000

# Define the processing time matrix T
T = [
    [9, 11, 8, 6],
    [13, 17, 12, 10],
    [15, 18, 14, 12],
    [20, 24, 18, 15],
]

# Create a model
mdl = Model("manne cplex")

# Create variables
C = {(r, i): mdl.continuous_var(lb=0) for r in range(n) for i in range(n)}
D = [[mdl.binary_var() for _ in range(n)] for _ in range(n)]
Cmax = mdl.continuous_var(lb=0)

# Objective function
mdl.minimize(Cmax)

# Constraints
for i in range(n):
    mdl.add_constraint(C[(0, i)] >= T[0][i])

for r in range(1, n):
    for i in range(n):
        mdl.add_constraint(C[(r, i)] - C[(r-1, i)] >= T[r][i])

for r in range(n):
    for k in range(1, n):
        for i in range(k):
            mdl.add_constraint(C[(r, i)] - C[(r, k)] + P*(1 - D[i][k]) >= T[r][i])
            mdl.add_constraint(C[(r, i)] - C[(r, k)] + P*(1 - D[i][k]) <= P - T[r][k])

for i in range(n):
    mdl.add_constraint(Cmax >= C[(n-1, i)])

# Solve the model
solution = mdl.solve()

# Print the solution
if solution:
    print(f"Solution status: {mdl.get_solve_status()}")
    print(f"Objective value: {solution.objective_value}")
    # for r in range(n):
    #     for i in range(n):
    #         print(f"C[{r}][{i}]: {C[(r, i)].solution_value}")
    # for i in range(n):
    #     for k in range(n):
    #         print(f"D[{i}][{k}]: {D[i][k].solution_value}")
else:
    print("No solution found")
