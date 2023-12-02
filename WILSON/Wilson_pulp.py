from pulp import *

# Variables
N = 4
M = 4
T = [
    [9, 11, 8, 6],
    [13, 17, 12, 10],
    [15, 18, 14, 12],
    [20, 24, 18, 15]
]

# Convertir la matriz T en un diccionario que será usado en las restricciones
T_dict = {(i, j): T[i][j] for i in range(N) for j in range(M)}

# Crear el problema
prob = LpProblem("Wilson_Model", LpMinimize)

# Definir las variables de decisión
Z = LpVariable.dicts("Z", ((i, j) for i in range(N) for j in range(M)), 0, 1, LpBinary)
B = LpVariable.dicts("B", ((i, j) for i in range(N) for j in range(M)), 0)

# Función objetivo
prob += B[(N-1, M-1)] + lpSum(T_dict[(N-1, i)] * Z[(i, M-1)] for i in range(N))  #De acuerdo a la formulación, asumo que B_MN es B en la última máquina y trabajo.

# Restricciones
for i in range(N):
    prob += lpSum(Z[(i, j)] for j in range(M)) == 1

for j in range(M):
    prob += lpSum(Z[(i, j)] for i in range(N)) == 1

B[(0,0)] = 0

for j in range(M-1):
    prob += B[(0, j)] + lpSum(T_dict[(0, i)] * Z[(i, j)] for i in range(N)) == B[(0, j+1)]

for r in range(N-1):
    prob += B[(r, 0)] + lpSum(T_dict[(r, i)] * Z[(i, 0)] for i in range(N)) == B[(r+1, 0)]

for r in range(N-1):
    for j in range(1, M):
        prob += B[(r, j)] + lpSum(T_dict[(r, i)] * Z[(i, j)] for i in range(N)) <= B[(r+1, j)]

for r in range(1, N):
    for j in range(M-1):
        prob += B[(r, j)] + lpSum(T_dict[(r, i)] * Z[(i, j)] for i in range(N)) <= B[(r, j+1)]

# Resolver el problema
prob.solve()

# Imprimir el estado de la solución
print("Status:", LpStatus[prob.status])

# Imprimir las variables de decisión
for v in prob.variables():
    print(v.name, "=", v.varValue)

# Imprimir la función objetivo
print("Objective =", value(prob.objective))
