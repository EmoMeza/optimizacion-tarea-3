from gurobipy import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import numpy as np

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

B[0, 0].setAttr(GRB.Attr.Start, 0)

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
tiempo_wilson = time.time()
m.optimize()
tiempo_wilson = time.time() - tiempo_wilson
# Imprimir el estado de la solución
print('Status:', m.status)

# Imprimir las variables de decisión
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

# Imprimir la función objetivo
print('Obj: %g' % m.objVal)
print('Tiempo de ejecución:', tiempo_wilson)

# Recoger los trabajos asignados a cada máquina y los tiempos de inicio/fin
jobs_machine = {(k[0], k[1]): k[1] for k, v in Z.items() if v.x > 0}
B_values = {k: v.x for k, v in B.items()}

# Generar los colores
colors = plt.cm.viridis(np.linspace(0, 1, N))

jobs_per_machine = {i: sorted([(k, B_values[k]) for k, v in B.items() if k[1] == i], key=lambda x: x[1]) for i in range(M)}

fig, ax = plt.subplots()
end_previous_job = {i: 0 for i in range(M)}
bar_height = 0.2  # Hacer las barras más delgadas

# Inicializar una lista vacía para mantener un registro de los trabajos que ya hemos añadido a la leyenda
jobs_in_legend = []

for machine, tasks in jobs_per_machine.items():
    for idx, task in enumerate(tasks):
        job = task[0]
        end_time = task[1]

        if end_time < end_previous_job[machine]:
            start_time = end_previous_job[machine]
        else:
            start_time = end_time - T[job[0]][machine]

        end_previous_job[machine] = start_time + T[job[0]][machine]

        # Agregar la leyenda solo la primera vez que dibujamos cada trabajo
        if job[0] not in jobs_in_legend:
            ax.broken_barh([(start_time, T[job[0]][machine])], (machine - 0.4 + idx * bar_height, bar_height), facecolors=colors[job[0] % len(colors)], label=f'J{job[0]+1}')
            jobs_in_legend.append(job[0])
        else:
            ax.broken_barh([(start_time, T[job[0]][machine])], (machine - 0.4 + idx * bar_height, bar_height), facecolors=colors[job[0] % len(colors)])

ax.set_xlabel('Tiempo')
ax.set_ylabel('Maquinas')
ax.set_yticks(range(M))
ax.set_yticklabels([f'Maquina {i+1}' for i in range(M)])
plt.grid(True)
ax.legend(bbox_to_anchor=(1.15, 1))  # Mueve la leyenda hacia la derecha de la gráfica
plt.show()