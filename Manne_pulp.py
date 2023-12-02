from pulp import *

# Datos del problema
T = [[9, 13, 15, 20],
     [11, 17, 18, 24],
     [8, 12, 14, 18],
     [6, 10, 12, 15]]

N = len(T)
M = len(T[0])
P = 10000  # Un número lo suficientemente grande

# Crear el problema
prob = LpProblem("ManneModel", LpMinimize)

# Variables de decisión
C = LpVariable.dicts("C", ((i, j) for i in range(N) for j in range(M)), lowBound=0)
D = LpVariable.dicts("D", ((i, j) for i in range(N) for j in range(N) if i < j), cat='Binary')
Cmax = LpVariable("Cmax", lowBound=0)

# Función objetivo
prob += Cmax

# Restricciones
for i in range(N):
    prob += C[i, 0] >= T[i][0]

for r in range(1, M):
    for i in range(N):
        prob += C[i, r] - C[i, r-1] >= T[i][r]

for r in range(M):
    for i in range(N):
        for k in range(i+1, N):
            prob += C[i, r] - C[k, r] + P*D[i, k] >= T[i][r]
            prob += C[k, r] - C[i, r] + P*(1 - D[i, k]) >= T[k][r]

for i in range(N):
    prob += Cmax >= C[i, M-1]

# Resolver el problema
prob.solve()

# Imprimir el estado de la solución
print("Status:", LpStatus[prob.status])

# Mostrar valores de la solución
print(f"Cmax: {Cmax.varValue}")
for i in range(N):
    for j in range(M):
        print(f"C[{i+1},{j+1}]: {C[i,j].varValue}")