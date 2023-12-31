import time
import gurobipy as gp
from gurobipy import GRB

# Definir el número de tareas y máquinas
# Como son 4 y 4 se deja en una sola variable
n = 4

# Definir una constante grande
P = 10000

# Definir la matriz de tiempos de procesamiento T
T = [
    [9, 11, 8, 6],
    [13, 17, 12, 10],
    [15, 18, 14, 12],
    [20, 24, 18, 15],
]

# Crear un modelo
model = gp.Model("manne")

# Crear variables
C = {(r, i): model.addVar(lb=0, vtype=GRB.CONTINUOUS) for r in range(n) for i in range(n)}
D = [[model.addVar(vtype=GRB.BINARY) for _ in range(n)] for _ in range(n)]
Cmax = model.addVar(lb=0, vtype=GRB.CONTINUOUS)

# Función objetivo
model.setObjective(Cmax, GRB.MINIMIZE)

# Restricciones
# (13)
for i in range(n):
    model.addConstr(C[(0, i)] >= T[0][i])

# (14)
for r in range(1, n):
    for i in range(n):
        model.addConstr(C[(r, i)] - C[(r-1, i)] >= T[r][i])

# (15) y (16)
for r in range(n):
    for k in range(1, n):
        for i in range(k):
            model.addConstr(C[(r, i)] - C[(r, k)] + P*(1 - D[i][k]) >= T[r][i])
            model.addConstr(C[(r, i)] - C[(r, k)] + P*(1 - D[i][k]) <= P - T[r][k])

# (17)
for i in range(n):
    model.addConstr(Cmax >= C[(n-1, i)])


# Comenzar a medir el tiempo
start_time = time.time()

# Optimizar el modelo
model.optimize()

# Terminar de medir el tiempo
end_time = time.time()
tiempoManneGUROBI = end_time - start_time

# Guardamos el valor de la función objetivo
solucionManneGUROBI = model.objVal

# Imprimir el tiempo
print(f"Tiempo: {tiempoManneGUROBI}")

# Imprimir la solución
if model.status == GRB.OPTIMAL:
    print(f"Valor objetivo: {model.objVal}")
    # for r in range(n):
    #     for i in range(n):
    #         print(f"C[{r}][{i}]: {C[(r, i)].X}")
    # for i in range(n):
    #     for k in range(n):
    #         print(f"D[{i}][{k}]: {D[i][k].X}")
else:
    print("No se encontró solución")

# Gráfico de Gantt
import matplotlib.pyplot as plt
import numpy as np

# Crear la matriz de tiempos
matrix = []
for r in range(n):
    machine = []
    for i in range(n):
        machine.append([C[(r, i)].X - T[r][i], C[(r, i)].X])
    matrix.append(machine)

# Crear el gráfico con Matplotlib
fig, gantt = plt.subplots(figsize=(10, 5))
gantt.set_title('Manne Gurobi')  # Añadir este título
gantt.set_xlabel('Tiempo')
gantt.set_ylabel('Máquinas')
gantt.set_xlim(0, model.objVal)
gantt.set_ylim(0, n * 10)
gantt.set_yticks(np.arange(5, n * 10, 10))
gantt.set_yticklabels(['M' + str(i) for i in range(1, n+1)])
gantt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)

# Definir colores para las barras de Gantt
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# Iterar sobre máquinas y trabajos para crear las barras
for r in range(n):
    for j in range(n):
        start = matrix[r][j][0]
        duration = matrix[r][j][1] - matrix[r][j][0]
        gantt.broken_barh([(start, duration)], ((r) * 10, 9), facecolors=colors[j])
        gantt.text(x=(start + duration/4), y=((r) * 10 + 6), s='Trabajo '+str(j+1), va='center', color='black')
        gantt.text(x=(start + duration/4), y=((r) * 10 + 3), s=str(duration), va='center', color='black')

# Mostrar el gráfico
plt.show()
