from docplex.mp.model import Model

N = 4  # Numero de trabajos
M = 4  # Numero de maquinas
T = [
    [9, 13, 15, 20], 
    [11, 17, 18, 24], 
    [8, 12, 14, 18], 
    [6, 10, 12, 15]  
]

mdl = Model(name="Liao-You_Model")

# Variables

S = mdl.continuous_var_matrix(M, N, name="S", lb=0)
D = mdl.binary_var_matrix(N, N, name="D")
q = mdl.continuous_var_cube(M, N, N, name="q", lb=0)
Cmax = mdl.continuous_var(name="Cmax", lb=0)

mdl.minimize(Cmax)

# Restricciones

for i in range(N):
    for r in range(M - 1):
        mdl.add_constraint(S[r, i] + T[i][r] <= S[r + 1, i])

P = 100000
for r in range(M):
    for i in range(N):
        for k in range(N):
            if i < k:
                mdl.add_constraint(S[r, i] - S[r, k] + P * D[i, k] - T[k][r] == q[r, i, k])
                mdl.add_constraint(P - T[i][r] - T[k][r] >= q[r, i, k])

# Restriccion para Cmax

for i in range(N):
    mdl.add_constraint(Cmax >= S[M - 1, i] + T[i][M - 1])

solution = mdl.solve(log_output=True)

# Resultados

if solution:
    print(f"Valor optimo de Cmax: {Cmax.solution_value}")
    for r in range(M):
        for i in range(N):
            print(f"Tiempo de inicio para el trabajo {i + 1} en la maquina {r + 1}: {S[r, i].solution_value}")
else:
    print("El problema no se resolvio de manera optima.")
