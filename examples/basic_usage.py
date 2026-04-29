import logging

from mdfh import MDFHSetCoverSolver

logging.basicConfig(level=logging.INFO)

variables = ["x1", "x2", "x3", "x4"]

fitness_cost_component = {
    "x1": 10.0,
    "x2": 8.0,
    "x3": 12.0,
    "x4": 7.0,
}

fitness_time_component = {
    "x1": 5.0,
    "x2": 3.0,
    "x3": 6.0,
    "x4": 4.0,
}

fitness_route_component = {
    "x1": 2.0,
    "x2": 1.0,
    "x3": 3.0,
    "x4": 2.0,
}

coverage_weight = {
    "x1": {"x2"},
    "x2": {"x1", "x3"},
    "x3": {"x4"},
    "x4": {"x3"},
}

solver = MDFHSetCoverSolver(
    variables=variables,
    fitness_cost_component=fitness_cost_component,
    fitness_time_component=fitness_time_component,
    fitness_route_component=fitness_route_component,
    coverage_weight=coverage_weight,
    include_self=True,
)

result = solver.solve(verbose=True)

print("Selected variables:", result.selected_variables)
print("Covered variables:", result.covered_variables)
print("Uncovered variables:", result.uncovered_variables)
print("Is feasible:", result.is_feasible)
print("Objective value:", result.objective_value)
print("Solve duration:", result.solve_duration)
