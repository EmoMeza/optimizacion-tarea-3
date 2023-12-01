from pulp import LpVariable, LpProblem, lpSum, value, minimize
from docplex.mp.model import Model
from gurobipy import Model as GurobiModel, GRB, quicksum

def manne_model_pulp(num_jobs, num_machines, processing_times):
    # Crear un problema de programación lineal
    model = LpProblem(name="Manne_Model", sense=minimize)

    # Índices para los trabajos, máquinas y posiciones en la secuencia
    jobs = range(num_jobs)
    machines = range(num_machines)
    positions = range(num_jobs)

    # Variables binarias para la asignación de trabajos a posiciones en las secuencias
    x = {(j, m, k): LpVariable(name=f"x_{j}_{m}_{k}", cat="Binary") for j in jobs for m in machines for k in positions}

    # Variables continuas para los tiempos de inicio de cada trabajo en cada máquina
    start_times = {(j, m): LpVariable(name=f"start_time_{j}_{m}", lowBound=0, cat="Continuous") for j in jobs for m in machines}

    # Función objetivo: minimizar el makespan
    model += lpSum(start_times[j, m] + processing_times[j][m] for j in jobs for m in machines)

    # Restricciones para garantizar la asignación correcta de trabajos a posiciones
    for j in jobs:
        for k in positions:
            model += lpSum(x[j, m, k] for m in machines) == 1

    # Restricciones para garantizar que cada trabajo se procese exactamente una vez en cada máquina
    for j in jobs:
        for m in machines:
            model += lpSum(x[j, m, k] for k in positions) == 1

    # Restricciones para garantizar que se respeten las restricciones de precedencia
    for j in jobs:
        for k in range(1, num_jobs):
            model += start_times[j, k] >= start_times[j, k - 1] + processing_times[j][k - 1]

    # Resolver el modelo con PuLP
    model.solve()

    # Imprimir los resultados
    print("Status:", model.status)
    print("Objective Value:", value(model.objective))

    # Imprimir la asignación de trabajos a posiciones en las secuencias
    for j in jobs:
        for m in machines:
            for k in positions:
                if value(x[j, m, k]) == 1:
                    print(f"Job {j + 1} assigned to position {k + 1} on machine {m + 1}")

    # Imprimir los tiempos de inicio
    for j in jobs:
        for m in machines:
            print(f"Start time for Job {j + 1} on Machine {m + 1}: {value(start_times[j, m])}")


# Resolver el modelo de Manne con PuLP y los datos de ejemplo
num_jobs_example = 4
num_machines_example = 4
processing_times_example = [
    [9, 13, 15, 20],
    [11, 17, 18, 24],
    [8, 12, 14, 18],
    [6, 10, 12, 15]
]

manne_model_pulp(num_jobs_example, num_machines_example, processing_times_example)

# Ahora, sección para CPLEX
def manne_model_cplex(num_jobs, num_machines, processing_times):
    # Crear un modelo
    model = Model(name="Manne_Model")

    # Índices para los trabajos, máquinas y posiciones en la secuencia
    jobs = range(num_jobs)
    machines = range(num_machines)
    positions = range(num_jobs)

    # Variables binarias para la asignación de trabajos a posiciones en las secuencias
    x = {(j, m, k): model.binary_var(name=f"x_{j}_{m}_{k}") for j in jobs for m in machines for k in positions}

    # Variables continuas para los tiempos de inicio de cada trabajo en cada máquina
    start_times = {(j, m): model.continuous_var(name=f"start_time_{j}_{m}") for j in jobs for m in machines}

    # Función objetivo: minimizar el makespan
    model.minimize(model.sum(start_times[j, m] + processing_times[j][m] for j in jobs for m in machines))

    # Restricciones para garantizar la asignación correcta de trabajos a posiciones
    for j in jobs:
        for k in positions:
            model.add_constraint(model.sum(x[j, m, k] for m in machines) == 1)

    # Restricciones para garantizar que cada trabajo se procese exactamente una vez en cada máquina
    for j in jobs:
        for m in machines:
            model.add_constraint(model.sum(x[j, m, k] for k in positions) == 1)

    # Restricciones para garantizar que se respeten las restricciones de precedencia
    for j in jobs:
        for k in range(1, num_jobs):
            model.add_constraint(start_times[j, k] >= start_times[j, k - 1] + processing_times[j][k - 1])

    # Resolver el modelo con CPLEX
    model.solve()

    # Imprimir los resultados
    print("Status:", model.solve_details.status)
    print("Objective Value:", model.objective_value)

    # Imprimir la asignación de trabajos a posiciones en las secuencias
    for j in jobs:
        for m in machines:
            for k in positions:
                if x[j, m, k].solution_value == 1:
                    print(f"Job {j + 1} assigned to position {k + 1} on machine {m + 1}")

    # Imprimir los tiempos de inicio
    for j in jobs:
        for m in machines:
            print(f"Start time for Job {j + 1} on Machine {m + 1}: {start_times[j, m].solution_value}")


# Resolver el modelo de Manne con CPLEX y los datos de ejemplo
manne_model_cplex(num_jobs_example, num_machines_example, processing_times_example)

# Ahora, sección para Gurobi
def manne_model_gurobi(num_jobs, num_machines, processing_times):
    # Crear un modelo
    model = GurobiModel()

    # Desactivar la salida en la consola de Gurobi
    model.setParam('OutputFlag', 0)

    # Índices para los trabajos, máquinas y posiciones en la secuencia
    jobs = range(num_jobs)
    machines = range(num_machines)
    positions = range(num_jobs)

    # Variables binarias para la asignación de trabajos a posiciones en las secuencias
    x = {(j, m, k): model.addVar(vtype=GRB.BINARY, name=f"x_{j}_{m}_{k}") for j in jobs for m in machines for k in positions}

    # Variables continuas para los tiempos de inicio de cada trabajo en cada máquina
    start_times = {(j, m): model.addVar(vtype=GRB.CONTINUOUS, name=f"start_time_{j}_{m}") for j in jobs for m in machines}

    # Agregar variables al modelo
    model.update()

    # Función objetivo: minimizar el makespan
    model.setObjective(quicksum(start_times[j, m] + processing_times[j][m] for j in jobs for m in machines), GRB.MINIMIZE)

    # Restricciones para garantizar la asignación correcta de trabajos a posiciones
    for j in jobs:
        for k in positions:
            model.addConstr(quicksum(x[j, m, k] for m in machines) == 1)

    # Restricciones para garantizar que cada trabajo se procese exactamente una vez en cada máquina
    for j in jobs:
        for m in machines:
            model.addConstr(quicksum(x[j, m, k] for k in positions) == 1)

    # Restricciones para garantizar que se respeten las restricciones de precedencia
    for j in jobs:
        for k in range(1, num_jobs):
            model.addConstr(start_times[j, k] >= start_times[j, k - 1] + processing_times[j][k - 1])

    # Optimizar el modelo con Gurobi
    model.optimize()

    # Imprimir los resultados
    print("Status:", model.status)
    print("Objective Value:", model.objVal)

    # Imprimir la asignación de trabajos a posiciones en las secuencias
    for j in jobs:
        for m in machines:
            for k in positions:
                if x[j, m, k].x == 1:
                    print(f"Job {j + 1} assigned to position {k + 1} on machine {m + 1}")

    # Imprimir los tiempos de inicio
    for j in jobs:
        for m in machines:
            print(f"Start time for Job {j + 1} on Machine {m + 1}: {start_times[j, m].x}")


# Resolver el modelo de Manne con Gurobi y los datos de ejemplo
manne_model_gurobi(num_jobs_example, num_machines_example, processing_times_example)
