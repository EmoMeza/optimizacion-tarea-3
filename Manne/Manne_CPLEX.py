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

# Gantt chart
import matplotlib.pyplot as plt
import numpy as np

matrix = []
for r in range(n):
    machine = []
    for i in range(n):
        machine.append([C[(r, i)].solution_value - T[r][i], C[(r, i)].solution_value])
    matrix.append(machine)

fig, gantt = plt.subplots(figsize=(10, 5))
gantt.set_title('Manne CPLEX')  # Add this line to set the title
gantt.set_xlabel('Time')
gantt.set_ylabel('Machines')
gantt.set_xlim(0, solution.objective_value)
gantt.set_ylim(0, n * 10)
gantt.set_yticks(np.arange(5, n * 10, 10))
gantt.set_yticklabels(['M' + str(i) for i in range(1, n+1)])
gantt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']  # Define as many colors as you have jobs

for r in range(n):
    for j in range(n):
        start = matrix[r][j][0]
        duration = matrix[r][j][1] - matrix[r][j][0]
        gantt.broken_barh([(start, duration)], ((r) * 10, 9), facecolors=colors[j])
        gantt.text(x=(start + duration/4), y=((r) * 10 + 6), s='Trabajo '+str(j+1), va='center', color='black')
        gantt.text(x=(start + duration/4), y=((r) * 10 + 3), s=str(duration), va='center', color='black')

plt.show()