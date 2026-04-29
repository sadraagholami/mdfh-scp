# mdfh-scp

A Multidimensional Fitness Heuristic solver for Set Covering Problems.

## Overview

`mdfh-scp` is a lightweight Python implementation of a Multidimensional Fitness
Heuristic for Set Covering Problems.

The implementation is inspired by the heuristic algorithm presented in:

> Hashemi et al. (2025), "A multidimensional fitness function based heuristic
> algorithm for set covering problems", Applied Soft Computing.

## Installation from GitHub

You can install and use this project directly from GitHub.

### 1. Clone the Repository
```bash
git clone https://github.com/sadraagholami/mdfh-scp.git
cd mdfh-scp
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to avoid dependency conflicts.

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the Package

Install the package in editable mode:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

If you want to install development dependencies, run:

```bash
python -m pip install -r requirements-dev.txt
```

## Usage

```python
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
```

## API

### `MDFHSetCoverSolver`

```python
MDFHSetCoverSolver(
variables,
fitness_cost_component,
fitness_time_component,
fitness_route_component,
coverage_weight,
include_self=True,
)
```

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

```python
MDFHResult(
selected_variables,
covered_variables,
uncovered_variables,
is_feasible,
objective_value,
solve_duration,
)
```
## Exceptions

- `MDFHValidationError`: Raised for invalid input data.
- `MDFHSolverError`: Raised when the solver cannot continue.
- `MDFHBaseException`: Base class for MDFH exceptions.

## Citation

```bibtex
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
```
## Disclaimer

This is an independent implementation and is not an official implementation
provided by the authors of the referenced paper.

## Contributing

Contributions are welcome. If you would like to improve this project, fix bugs, add features, improve documentation, or add tests, please follow the steps below.

### Fork the Repository

Click the **Fork** button at the top-right of the repository page on GitHub.

This creates a copy of the repository under your own GitHub account.

### Make Your Changes

You can contribute by:

- Fixing bugs
- Adding new examples
- Improving documentation
- Adding tests
- Improving code structure
- Adding new features
- Improving validation or error handling

Please keep the code clear, readable, and well documented.

## Reporting Issues

If you find a bug or have a suggestion, please open an issue on GitHub:
```text
https://github.com/sadraagholami/mdfh-scp/issues

When reporting a bug, please include:

- A clear description of the problem
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Python version
- Operating system
- Any relevant error messages
```

## License

MIT License.


