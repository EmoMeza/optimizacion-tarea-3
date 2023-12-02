import pulp

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

# Resolver
problema.solve(pulp.PULP_CBC_CMD(msg=0))

# Print the results
print("Status:", pulp.LpStatus[problema.status])
print("Objective value:", pulp.value(problema.objective))
print("Cmax:", pulp.value(Cmax))
# print("C matrix:")
# for r in range(M):
#     for i in range(N):
#         print(pulp.value(C[(r, i)]), end=" ")
#     print()
