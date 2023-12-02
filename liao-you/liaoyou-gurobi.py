from gurobipy import Model, GRB

N = 4  # Numero de trabajos
M = 4  # Numero de maquinas
T = [
    [9, 13, 15, 20],
    [11, 17, 18, 24], 
    [8, 12, 14, 18],  
    [6, 10, 12, 15]   
]

mdl = Model("Liao-You_Model")

# Variables

S = mdl.addVars(M, N, vtype=GRB.CONTINUOUS, name="S")
q = mdl.addVars(M, N, N, vtype=GRB.CONTINUOUS, name="q")
D = mdl.addVars(N, N, vtype=GRB.BINARY, name="D")
Cmax = mdl.addVar(vtype=GRB.CONTINUOUS, name="Cmax")

mdl.setObjective(Cmax, GRB.MINIMIZE)

# Restricciones

for i in range(N):
    for r in range(M - 1):
        mdl.addConstr(S[r, i] + T[i][r] <= S[r + 1, i])

P = 100000
for r in range(M):
    for i in range(N):
        for k in range(N):
            if i < k:
                mdl.addConstr(S[r, i] - S[r, k] + P * D[i, k] - T[k][r] == q[r, i, k])
                mdl.addConstr(P - T[i][r] - T[k][r] >= q[r, i, k])

# Restriccion para Cmax

for i in range(N):
    mdl.addConstr(Cmax >= S[M - 1, i] + T[i][M - 1])

mdl.optimize()

# Resultados

if mdl.status == GRB.OPTIMAL:
    print(f"Valor optimo de Cmax: {Cmax.X}")
    for r in range(M):
        for i in range(N):
            print(f"Tiempo de inicio para el trabajo {i + 1} en la maquina {r + 1}: {S[r, i].X}")
else:
    print("El problema no se resolvio de manera optima.")
