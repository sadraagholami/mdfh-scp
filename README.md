# mdfh-scp

A Multidimensional Fitness Heuristic solver for Set Covering Problems.

## Overview

`mdfh-scp` is a lightweight Python implementation of a Multidimensional Fitness
Heuristic for Set Covering Problems.

The implementation is inspired by the heuristic algorithm presented in:

> Hashemi et al. (2025), "A multidimensional fitness function based heuristic
> algorithm for set covering problems", Applied Soft Computing.

## Installation
```bash
pip install mdfh-scp

## Usage

python
from mdfh import MDFHSetCoverSolver

variables = ["x1", "x2", "x3"]

fitness_cost_component = {
"x1": 10.0,
"x2": 8.0,
"x3": 6.0,
}

fitness_time_component = {
"x1": 1.0,
"x2": 1.0,
"x3": 1.0,
}

fitness_route_component = {
"x1": 1.0,
"x2": 1.0,
"x3": 1.0,
}

coverage_weight = {
"x1": {"x2"},
"x2": {"x1", "x3"},
"x3": {"x3"},
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

print(result.selected_variables)
print(result.objective_value)
print(result.is_feasible)

## API

### `MDFHSetCoverSolver`

python
MDFHSetCoverSolver(
variables,
fitness_cost_component,
fitness_time_component,
fitness_route_component,
coverage_weight,
include_self=True,
)

### Parameters

- `variables`: List of variable identifiers.
- `fitness_cost_component`: Cost-related fitness component.
- `fitness_time_component`: Time-related fitness component.
- `fitness_route_component`: Route-related fitness component.
- `coverage_weight`: Mapping of each variable to the variables it covers.
- `include_self`: If `True`, each variable covers itself.

### `solve(verbose=False)`

Runs the MDFH heuristic and returns an `MDFHResult`.

## Result Object

The solver returns:

python
MDFHResult(
selected_variables,
covered_variables,
uncovered_variables,
is_feasible,
objective_value,
solve_duration,
)

## Exceptions

- `MDFHValidationError`: Raised for invalid input data.
- `MDFHSolverError`: Raised when the solver cannot continue.
- `MDFHBaseException`: Base class for MDFH exceptions.

## Citation

bibtex
@article{hashemi2025multidimensional,
  title = {A multidimensional fitness function based heuristic algorithm for set covering problems},
  author = {Hashemi, A. and Gholami, H. and Delorme, X. and Wong, K. Y.},
  journal = {Applied Soft Computing},
  volume = {174},
  pages = {113038},
  year = {2025},
  issn = {1568-4946},
  doi = {10.1016/j.asoc.2025.113038}
}

## Disclaimer

This is an independent implementation and is not an official implementation
provided by the authors of the referenced paper.

## License

MIT License.


