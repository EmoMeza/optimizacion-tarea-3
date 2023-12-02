from gurobipy import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Variables
N = 4
M = 4
T = [
    [9, 11, 8, 6],
    [13, 17, 12, 10],
    [15, 18, 14, 12],
    [20, 24, 18, 15]
]

# Crea el modelo
m = Model("Wilson_Model")

# Definir las variables de decisión
Z = m.addVars(N, M, vtype=GRB.BINARY, name="Z")
B = m.addVars(N, M, vtype=GRB.CONTINUOUS, name="B")

# Función objetivo
m.setObjective(B[N-1, M-1] + quicksum(T[N-1][i]*Z[i, M-1] for i in range(N)), GRB.MINIMIZE)

# Restricciones
for i in range(N):
    m.addConstr(quicksum(Z[i, j] for j in range(M)) == 1)

for j in range(M):
    m.addConstr(quicksum(Z[i, j] for i in range(N)) == 1)

B[0, 0] = 0

for j in range(M-1):
    m.addConstr(B[0, j] + quicksum(T[0][i] * Z[i, j] for i in range(N)) == B[0, j+1])

for r in range(N-1):
    m.addConstr(B[r, 0] + quicksum(T[r][i] * Z[i, 0] for i in range(N)) == B[r+1, 0])

for r in range(N-1):
    for j in range(1, M):
        m.addConstr(B[r, j] + quicksum(T[r][i] * Z[i, j] for i in range(N)) <= B[r+1, j])

for r in range(1, N):
    for j in range(M-1):
        m.addConstr(B[r, j] + quicksum(T[r][i] * Z[i, j] for i in range(N)) <= B[r, j+1])

# Resolver el problema
m.optimize()

# Imprimir el estado de la solución
print('Status:', m.status)

# Imprimir las variables de decisión
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

# Imprimir la función objetivo
print('Obj: %g' % m.objVal)