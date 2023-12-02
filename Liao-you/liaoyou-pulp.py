import pulp

N = 4  # Numero de trabajos
M = 4  # Numero de maquinas
T = [
    [9, 13, 15, 20],  
    [11, 17, 18, 24], 
    [8, 12, 14, 18],  
    [6, 10, 12, 15]   
]

problem = pulp.LpProblem("Liao-You_Model", pulp.LpMinimize)

# Variables

S = pulp.LpVariable.dicts("S", ((r, i) for r in range(M) for i in range(N)), 0)
q = pulp.LpVariable.dicts("q", ((r, i, k) for r in range(M) for i in range(N) for k in range(N) if i != k), 0)
D = pulp.LpVariable.dicts("D", ((i, k) for i in range(N) for k in range(N) if i != k), 0, 1, pulp.LpBinary)
Cmax = pulp.LpVariable("Cmax", 0)

problem += Cmax

# Restricciones

for i in range(N):
    for r in range(M - 1):
        problem += S[r, i] + T[i][r] <= S[r + 1, i]

P = 100000
for r in range(M):
    for i in range(N):
        for k in range(N):
            if i < k:
                problem += S[r, i] - S[r, k] + P * D[i, k] - T[k][r] == q[r, i, k]
                problem += P - T[i][r] - T[k][r] >= q[r, i, k]

# Restriccion para Cmax

for i in range(N):
    problem += Cmax >= S[M - 1, i] + T[i][M - 1]

problem.solve()

# Resultados

if problem.status == 1:
    print(f"Valor optimo de Cmax: {Cmax.value()}")
    for r in range(M):
        for i in range(N):
            print(f"Tiempo de inicio para el trabajo {i + 1} en la maquina {r + 1}: {S[r, i].value()}")
else:
    print("El problema no se resolvio de manera optima.")
