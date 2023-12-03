import pulp
import pulp as lp
import time
import matplotlib.pyplot as plt
import numpy as np
# Matriz T transpuesta
T = [
    [9, 11, 8, 6],
    [13, 17, 12, 10],
    [15, 18, 14, 12],
    [20, 24, 18, 15],
]

# Constants
M = len(T[0])  # máquinas
N = len(T)     # trabajos

# Modelo Manne con PuLP
problema = pulp.LpProblem("PFSP", pulp.LpMinimize)

# Variables
P = 1000
D = pulp.LpVariable.dicts("D", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
C = pulp.LpVariable.dicts("C", ((i, j) for i in range(M) for j in range(N)), lowBound=0, cat='Continuous')

# Variable de completitud
Cmax = pulp.LpVariable("Cmax", lowBound=0, cat='Continuous')

# Función objetivo
problema += Cmax

# Restricciones
# (13)
for i in range(N):
    problema += C[0, i] >= T[0][i]

# (14)
for r in range(1, M):
    for i in range(N):
        problema += C[r, i] - C[r-1, i] >= T[r][i]

# (15) y (16)
for r in range(M):
    for k in range(N):
        for i in range(k):
            if i < k:
                problema += C[r, i] - C[r, k] + P * D[i, k] >= T[r][i]
                problema += C[r, i] - C[r, k] + P * D[i, k] <= P - T[r][k]

# (17)
for i in range(N):
    problema += Cmax >= C[M-1, i]


# Start timing
start_time = time.time()

# Resolver
problema.solve(pulp.PULP_CBC_CMD(msg=0))

# End timing
end_time = time.time()
elapsed_time = end_time - start_time

# Print the results
print("Status:", pulp.LpStatus[problema.status])
print("Objective value:", pulp.value(problema.objective))
print("Cmax:", pulp.value(Cmax))

# Gantt chart

matrix = []
for r in range(M):
    machine = []
    for i in range(N):
        machine.append([lp.value(C[r, i]) - T[r][i], lp.value(C[r, i])])
    matrix.append(machine)

fig, gantt = plt.subplots(figsize=(10, 5))
gantt.set_title('Manne PuLP')  # Add this line to set the title
gantt.set_xlabel('Time')
gantt.set_ylabel('Machines')
gantt.set_xlim(0, lp.value(problema.objective))
gantt.set_ylim(0, M * 10)
gantt.set_yticks(np.arange(5, M * 10, 10))
gantt.set_yticklabels(['M' + str(i) for i in range(1, M+1)])
gantt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']  # Define as many colors as you have jobs

for r in range(M):
    for j in range(N):
        start = matrix[r][j][0]
        duration = matrix[r][j][1] - matrix[r][j][0]
        gantt.broken_barh([(start, duration)], ((r) * 10, 9), facecolors=colors[j])
        gantt.text(x=(start + duration/4), y=((r) * 10 + 6), s='Trabajo '+str(j+1), va='center', color='black')
        gantt.text(x=(start + duration/4), y=((r) * 10 + 3), s=str(duration), va='center', color='black')


plt.show()