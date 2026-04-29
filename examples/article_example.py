from mdfh import MDFHSetCoverSolver

variables = [f"y{i}" for i in range(1,11)]

A = 1
B = 1
E = 1

f = {v: A for v in variables}
t = {v: B for v in variables}
n = {v: E for v in variables}

B_sets = {
"y1": {"y2","y3","y5","y6"},
"y2": {"y1","y3","y4"},
"y3": {"y1","y2","y4"},
"y4": {"y2","y3","y7","y8", "y9"},
"y5": {"y3","y4"},
"y6": {"y3","y4"},
"y7": {"y4","y5"},
"y8": {"y5","y6"},
"y9": {"y7","y8"},
"y10": {"y9"}
}

solver = MDFHSetCoverSolver(
    variables,
    f,
    t,
    n,
    B_sets,
    include_self=True
)

result = solver.solve(verbose=True)

print("Selected variables:", result.selected_variables)
print("Covered variables:", result.covered_variables)
print("Uncovered variables:", result.uncovered_variables)
print("Is feasible:", result.is_feasible)
print("Objective value:", result.objective_value)
print("Solve duration:", result.solve_duration)