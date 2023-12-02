from gurobipy import *

# Datos del problema
T = [[9, 13, 15, 20],
     [11, 17, 18, 24],
     [8, 12, 14, 18],
     [6, 10, 12, 15]]

N = len(T)
M = len(T[0])
P = 10000  # Un número lo suficientemente grande

# Inicializa el modelo
m = Model("ManneModel_Gurobi")

# Variables de decisión
C = m.addVars(N, M, name="C")
D = m.addVars(((i, j) for i in range(N) for j in range(i+1, N)), vtype=GRB.BINARY, name="D")
Cmax = m.addVar(name="Cmax")

# Función objetivo
m.setObjective(Cmax, GRB.MINIMIZE)

# Restricciones
for i in range(N):
    m.addConstr(C[i, 0] >= T[i][0])

for r in range(1, M):
    for i in range(N):
        m.addConstr(C[i, r] - C[i, r-1] >= T[i][r])

for r in range(M):
    for i in range(N):
        for k in range(i+1, N):
            m.addConstr(C[i, r] - C[k, r] + P*D[i, k] >= T[i][r])
            m.addConstr(C[k, r] - C[i, r] + P*(1 - D[i, k]) >= T[k][r])

for i in range(N):
    m.addConstr(Cmax >= C[i, M-1])

# Resolver el problema
m.optimize()

# Imprimir el estado de la solución
if m.status == GRB.OPTIMAL:
    print('Solución óptima encontrada')
elif m.status == GRB.INFEASIBLE:
    print('Modelo es infactible')
elif m.status == GRB.INF_OR_UNBD:
    print('Modelo es infactible o no acotado')
elif m.status == GRB.UNBOUNDED:
    print('Modelo es no acotado')
else:
    print('Optimización finalizada con estatus', m.status)

# Mostrar valores de la solución
print(f"Cmax: {Cmax.x}")
for i in range(N):
    for j in range(M):
        print(f"C[{i+1},{j+1}]: {C[i,j].x}")