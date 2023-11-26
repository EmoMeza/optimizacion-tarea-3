from pulp import LpVariable, LpProblem, LpMinimize, lpSum

# Datos del problema
trabajo_maquinas = {
    'J1': [9, 13, 15, 20],
    'J2': [11, 17, 18, 24],
    'J3': [8, 12, 14, 18],
    'J4': [6, 10, 12, 15],
}

trabajos = list(trabajo_maquinas.keys())
maquinas = range(len(trabajo_maquinas['J1']))

# Crear el modelo de Wagner
modelo_wagner = LpProblem(name="Wagner_Model", sense=LpMinimize)

# Crear variables de decisión
x = LpVariable.dicts("x", ((i, j) for i in trabajos for j in maquinas), cat='Binary')

# Función objetivo
modelo_wagner += lpSum(x[i, j] for i in trabajos for j in maquinas)

# Restricciones
for i in trabajos:
    modelo_wagner += lpSum(x[i, j] for j in maquinas) == 1

for j in maquinas:
    modelo_wagner += lpSum(x[i, j] for i in trabajos) == 1

# Resolver el modelo con PuLP
modelo_wagner.solve()

# Presentar resultados
print(f"Status: {modelo_wagner.status}")
print(f"Valor de la función objetivo: {modelo_wagner.objective.value()}")

# Mostrar la carta Gantt (debes implementar esta parte)
# ...

# Puedes replicar este código para los otros modelos y solvers
