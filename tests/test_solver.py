import pytest

from mdfh import MDFHSetCoverSolver, MDFHValidationError


def test_solver_returns_feasible_solution():
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

    result = solver.solve()

    assert result.is_feasible is True
    assert set(result.selected_variables)
    assert result.covered_variables == set(variables)
    assert result.uncovered_variables == set()
    assert result.objective_value is not None
    assert result.solve_duration is not None


def test_missing_component_raises_validation_error():
    variables = ["x1", "x2"]

    with pytest.raises(MDFHValidationError):
        MDFHSetCoverSolver(
            variables=variables,
            fitness_cost_component={"x1": 1.0},
            fitness_time_component={"x1": 1.0, "x2": 1.0},
            fitness_route_component={"x1": 1.0, "x2": 1.0},
            coverage_weight={"x1": {"x2"}, "x2": {"x1"}},
        )


def test_unknown_coverage_variable_raises_validation_error():
    variables = ["x1", "x2"]

    with pytest.raises(MDFHValidationError):
        MDFHSetCoverSolver(
            variables=variables,
            fitness_cost_component={"x1": 1.0, "x2": 1.0},
            fitness_time_component={"x1": 1.0, "x2": 1.0},
            fitness_route_component={"x1": 1.0, "x2": 1.0},
            coverage_weight={"x1": {"x3"}, "x2": {"x1"}},
        )