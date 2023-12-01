from pulp import LpVariable, LpProblem, LpMinimize, lpSum

def solve_wagner_model(tri_values):
    num_jobs, num_machines = len(tri_values), len(tri_values[0])

    # Crear el problema de optimización
    problem = LpProblem(name="Wagner_Model", sense=LpMinimize)

    # Crear variables binarias para la asignación de trabajos a máquinas
    x = LpVariable.dicts("x", ((i, j) for i in range(num_jobs) for j in range(num_machines)), cat="Binary")

    # Definir la función objetivo (minimizar makespan)
    problem += lpSum(x[i, j] * tri_values[i][j] for i in range(num_jobs) for j in range(num_machines)), "Makespan"

    # Cada trabajo se asigna a exactamente una máquina
    for i in range(num_jobs):
        problem += lpSum(x[i, j] for j in range(num_machines)) == 1, f"Assign_{i}"

    # Cada máquina recibe exactamente un trabajo en cada paso de tiempo
    for j in range(num_machines):
        problem += lpSum(x[i, j] for i in range(num_jobs)) == 1, f"Machine_{j}"

    # Resolver el problema
    problem.solve()

    # Imprimir resultados
    print("Status:", problem.status)
    print("Objective Value (Makespan):", problem.objective.value())

    # Imprimir la asignación de trabajos a máquinas
    for i in range(num_jobs):
        for j in range(num_machines):
            if x[i, j].value() == 1:
                print(f"Job {i+1} assigned to Machine {j+1}")

def solve_wilson_model(tri_values):
    num_jobs, num_machines = len(tri_values), len(tri_values[0])

    # Crear el problema de optimización
    problem = LpProblem(name="Wilson_Model", sense=LpMinimize)

    # Crear variables binarias para la asignación de trabajos a máquinas
    x = LpVariable.dicts("x", ((i, j) for i in range(num_jobs) for j in range(num_machines)), cat="Binary")

    # Crear variables de inicio (start) y final (end) para cada trabajo en cada máquina
    start_time = LpVariable.dicts("start", (i for i in range(num_jobs)), lowBound=0, cat="Continuous")
    end_time = LpVariable.dicts("end", (i for i in range(num_jobs)), lowBound=0, cat="Continuous")

    # Definir la función objetivo (minimizar makespan)
    problem += end_time[num_jobs-1], "Makespan"

    # Restricciones de precedencia y tiempo de procesamiento
    for i in range(num_jobs):
        for j in range(num_machines):
            if i > 0:
                problem += start_time[i] >= end_time[i-1] + tri_values[i-1][j] - (1 - x[i, j]) * 1000, f"Precedence_{i}_{j}"
            problem += end_time[i] == start_time[i] + tri_values[i][j], f"Processing_{i}_{j}"

    # Cada trabajo se asigna a exactamente una máquina
    for i in range(num_jobs):
        problem += lpSum(x[i, j] for j in range(num_machines)) == 1, f"Assign_{i}"

    # Resolver el problema
    problem.solve()

    # Imprimir resultados
    print("Status:", problem.status)
    print("Objective Value (Makespan):", problem.objective.value())

    # Imprimir la asignación de trabajos a máquinas
    for i in range(num_jobs):
        for j in range(num_machines):
            if x[i, j].value() == 1:
                print(f"Job {i+1} assigned to Machine {j+1}")

def solve_manne_model(tri_values):
    num_jobs, num_machines = len(tri_values), len(tri_values[0])

    # Crear el problema de optimización
    problem = LpProblem(name="Manne_Model", sense=LpMinimize)

    # Crear variables binarias para la asignación de trabajos a máquinas
    x = LpVariable.dicts("x", ((i, j) for i in range(num_jobs) for j in range(num_machines)), cat="Binary")

    # Crear variables de inicio (start) y final (end) para cada trabajo en cada máquina
    start_time = LpVariable.dicts("start", (i for i in range(num_jobs)), lowBound=0, cat="Continuous")
    end_time = LpVariable.dicts("end", (i for i in range(num_jobs)), lowBound=0, cat="Continuous")

    # Definir la función objetivo (minimizar makespan)
    problem += end_time[num_jobs-1], "Makespan"

    # Restricciones de precedencia y tiempo de procesamiento
    for i in range(num_jobs):
        for j in range(num_machines):
            if i > 0:
                problem += start_time[i] >= end_time[i-1] + tri_values[i-1][j] - (1 - x[i, j]) * 1000, f"Precedence_{i}_{j}"
            problem += end_time[i] == start_time[i] + tri_values[i][j], f"Processing_{i}_{j}"

    # Cada trabajo se asigna a exactamente una máquina
    for i in range(num_jobs):
        problem += lpSum(x[i, j] for j in range(num_machines)) == 1, f"Assign_{i}"

    # Resolver el problema
    problem.solve()

    # Imprimir resultados
    print("Status:", problem.status)
    print("Objective Value (Makespan):", problem.objective.value())

    # Imprimir la asignación de trabajos a máquinas
    for i in range(num_jobs):
        for j in range(num_machines):
            if x[i, j].value() == 1:
                print(f"Job {i+1} assigned to Machine {j+1}")

def solve_liao_you_model(tri_values):
    num_jobs, num_machines = len(tri_values), len(tri_values[0])

    # Crear el problema de optimización
    problem = LpProblem(name="Liao_You_Model", sense=LpMinimize)

    # Crear variables binarias para la asignación de trabajos a máquinas
    x = LpVariable.dicts("x", ((i, j) for i in range(num_jobs) for j in range(num_machines)), cat="Binary")

    # Crear variables de inicio (start) y final (end) para cada trabajo en cada máquina
    start_time = LpVariable.dicts("start", (i for i in range(num_jobs)), lowBound=0, cat="Continuous")
    end_time = LpVariable.dicts("end", (i for i in range(num_jobs)), lowBound=0, cat="Continuous")

    # Definir la función objetivo (minimizar makespan)
    problem += end_time[num_jobs-1], "Makespan"

    # Restricciones de precedencia y tiempo de procesamiento
    for i in range(num_jobs):
        for j in range(num_machines):
            if i > 0:
                problem += start_time[i] >= end_time[i-1] + tri_values[i-1][j] - (1 - x[i, j]) * 1000, f"Precedence_{i}_{j}"
            problem += end_time[i] == start_time[i] + tri_values[i][j], f"Processing_{i}_{j}"

    # Cada trabajo se asigna a exactamente una máquina
    for i in range(num_jobs):
        problem += lpSum(x[i, j] for j in range(num_machines)) == 1, f"Assign_{i}"

    # Restricción de Liao-You (relacionada con el tiempo de procesamiento)
    for j in range(num_machines):
        for i in range(num_jobs):
            for k in range(i + 1, num_jobs):
                problem += end_time[i] + tri_values[i][j] <= start_time[k] + (1 - x[k, j]) * 1000, f"Liao_You_{i}_{j}_{k}"

    # Resolver el problema
    problem.solve()

    # Imprimir resultados
    print("Status:", problem.status)
    print("Objective Value (Makespan):", problem.objective.value())

    # Imprimir la asignación de trabajos a máquinas
    for i in range(num_jobs):
        for j in range(num_machines):
            if x[i, j].value() == 1:
                print(f"Job {i+1} assigned to Machine {j+1}")










tri_values_data = [
    [9, 13, 15, 20],
    [11, 17, 18, 24],
    [8, 12, 14, 18],
    [6, 10, 12, 15]
]



# solve_wagner_model(tri_values_data)
# solve_wilson_model(tri_values_data)
# solve_manne_model(tri_values_data)
# solve_liao_you_model(tri_values_data)