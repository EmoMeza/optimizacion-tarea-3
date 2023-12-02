import gurobipy as gp
from gurobipy import GRB

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
model = gp.Model("manne")

# Create variables
C = {(r, i): model.addVar(lb=0, vtype=GRB.CONTINUOUS) for r in range(n) for i in range(n)}
D = [[model.addVar(vtype=GRB.BINARY) for _ in range(n)] for _ in range(n)]
Cmax = model.addVar(lb=0, vtype=GRB.CONTINUOUS)

# Objective function
model.setObjective(Cmax, GRB.MINIMIZE)

# Constraints
for i in range(n):
    model.addConstr(C[(0, i)] >= T[0][i])

for r in range(1, n):
    for i in range(n):
        model.addConstr(C[(r, i)] - C[(r-1, i)] >= T[r][i])

for r in range(n):
    for k in range(1, n):
        for i in range(k):
            model.addConstr(C[(r, i)] - C[(r, k)] + P*(1 - D[i][k]) >= T[r][i])
            model.addConstr(C[(r, i)] - C[(r, k)] + P*(1 - D[i][k]) <= P - T[r][k])

for i in range(n):
    model.addConstr(Cmax >= C[(n-1, i)])

# Optimize the model
model.optimize()

# Print the solution
if model.status == GRB.OPTIMAL:
    print(f"Objective value: {model.objVal}")
    # for r in range(n):
    #     for i in range(n):
    #         print(f"C[{r}][{i}]: {C[(r, i)].X}")
    # for i in range(n):
    #     for k in range(n):
    #         print(f"D[{i}][{k}]: {D[i][k].X}")
else:
    print("No solution found")
