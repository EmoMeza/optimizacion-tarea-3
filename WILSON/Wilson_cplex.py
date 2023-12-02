from docplex.mp.model import Model

# Variables
N = 4
M = 4
T = [
    [9, 11, 8, 6],
    [13, 17, 12, 10],
    [15, 18, 14, 12],
    [20, 24, 18, 15]
]

# Crear el modelo
mdl = Model("Wilson_Model")

# Definir las variables de decisión
Z = mdl.binary_var_matrix(N, M, name="Z")
B = mdl.continuous_var_matrix(N, M, name="B")

# Función objetivo
mdl.minimize(B[N-1, M-1] + mdl.sum(T[N-1][i] * Z[i, M-1] for i in range(N)))

# Restricciones
for i in range(N):
    mdl.add_constraint(mdl.sum(Z[i, j] for j in range(M)) == 1)

for j in range(M):
    mdl.add_constraint(mdl.sum(Z[i, j] for i in range(N)) == 1)

B[0, 0] = 0

for j in range(M-1):
    mdl.add_constraint(B[0, j] + mdl.sum(T[0][i] * Z[i, j] for i in range(N)) == B[0, j+1])

for r in range(N-1):
    mdl.add_constraint(B[r, 0] + mdl.sum(T[r][i] * Z[i, 0] for i in range(N)) == B[r+1, 0])

for r in range(N-1):
    for j in range(1, M):
        mdl.add_constraint(B[r, j] + mdl.sum(T[r][i] * Z[i, j] for i in range(N)) <= B[r+1, j])

for r in range(1, N):
    for j in range(M-1):
        mdl.add_constraint(B[r, j] + mdl.sum(T[r][i] * Z[i, j] for i in range(N)) <= B[r, j+1])

# Resolver el problema
solution = mdl.solve()

# Imprimir el estado de la solución
print("Status:", "Optimal" if solution else "No solution found")

if solution:
    # Imprimir las variables de decisión
    for [var, val] in solution.iter_var_values():
        print(f"{var.name} = {val}")
    # Imprimir la función objetivo
    print("Objective =", solution.objective_value)