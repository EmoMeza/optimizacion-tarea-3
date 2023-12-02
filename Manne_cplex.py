from docplex.mp.model import Model

# Datos del problema
T = [[9, 13, 15, 20],
     [11, 17, 18, 24],
     [8, 12, 14, 18],
     [6, 10, 12, 15]]

N = len(T)
M = len(T[0])
P = 10000  # Un número lo suficientemente grande

# Crea el modelo
mdl = Model("ManneModel")

# Variables de decisión
C = mdl.continuous_var_matrix(N, M, name="C")
Cmax = mdl.continuous_var(name="Cmax")

# Declarar las variables 'D'
D = {(i, j): mdl.binary_var(name='D_{0}_{1}'.format(i, j))
     for i in range(N) for j in range(i+1, N)}

# Función objetivo
mdl.minimize(Cmax)

# Restricciones
for i in range(N):
    mdl.add_constraint(C[i, 0] >= T[i][0])

for r in range(1, M):
    for i in range(N):
        mdl.add_constraint(C[i, r] - C[i, r-1] >= T[i][r])

for r in range(M):
    for i in range(N):
        for k in range(i+1, N):
            mdl.add_constraint(C[i, r] - C[k, r] + P*D[i, k] >= T[i][r])
            mdl.add_constraint(C[k, r] - C[i, r] + P*(1 - D[i, k]) >= T[k][r])

for i in range(N):
    mdl.add_constraint(Cmax >= C[i, M-1])

# Resolver el problema
solution = mdl.solve(log_output=True)

# Mostrar valores de la solución
print(f"Cmax: {solution.get_value(Cmax)}")
for i in range(N):
    for j in range(M):
        print(f"C[{i+1},{j+1}]: {solution.get_value(C[i,j])}")