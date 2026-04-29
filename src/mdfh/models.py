"""Data models used by the MDFH set covering solver."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MDFHResult:
    """Result returned by the MDFH set covering solver.

    Attributes
    ----------
    selected_variables:
        Variables selected by the heuristic solution.

    covered_variables:
        Variables covered by the selected variables.

    uncovered_variables:
        Variables not covered by the selected variables.

    is_feasible:
        Whether all variables are covered.

    objective_value:
        Final objective value of the selected solution.

    solve_duration:
        Runtime of the solve process in seconds.
    """

    selected_variables: list[str]
    covered_variables: set[str]
    uncovered_variables: set[str]
    is_feasible: bool
    objective_value: float | None = None
    solve_duration: float | None = None
