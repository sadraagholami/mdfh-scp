"""Multidimensional Fitness Heuristic solver for set covering problems."""

from __future__ import annotations

import logging
import time
from typing import Dict, List, Set

from .exceptions import MDFHValidationError, MDFHSolverError
from .models import MDFHResult

logger = logging.getLogger(__name__)


class MDFHSetCoverSolver:
    """Multidimensional Fitness Heuristic solver for Set Covering Problems.

    This class implements a heuristic method based on a multidimensional
    fitness score. At each iteration, the algorithm selects a candidate
    variable with the highest computed fitness score and removes the variables
    covered by that selected variable from the candidate set.

    Parameters
    ----------
    variables:
        List of variable identifiers.

    fitness_cost_component:
        Mapping from each variable to its cost-related fitness component.

    fitness_time_component:
        Mapping from each variable to its time-related fitness component.

    fitness_route_component:
        Mapping from each variable to its route-related fitness component.

    coverage_weight:
        Mapping from each variable to the set of variables it covers.

    include_self:
        If True, each variable is considered to cover itself.
    """

    def __init__(
        self,
        variables: List[str],
        fitness_cost_component: Dict[str, float],
        fitness_time_component: Dict[str, float],
        fitness_route_component: Dict[str, float],
        coverage_weight: Dict[str, Set[str]],
        include_self: bool = True,
    ) -> None:
        self.variables = variables
        self.fitness_cost_component = fitness_cost_component
        self.fitness_time_component = fitness_time_component
        self.fitness_route_component = fitness_route_component
        self.coverage_weight = coverage_weight
        self.include_self = include_self

        self.y: dict[str, int] = {variable: 0 for variable in variables}
        self.candidate_variables: set[str] = set(variables)
        self.eliminated_variables: set[str] = set()

        self._validate_input()

    def _validate_input(self) -> None:
        """Validate solver input data.

        Raises
        ------
        MDFHValidationError
            If variables or component dictionaries are inconsistent.
        """

        if not self.variables:
            raise MDFHValidationError("The variables list cannot be empty.")

        variable_set = set(self.variables)

        if len(variable_set) != len(self.variables):
            raise MDFHValidationError("The variables list contains duplicate values.")

        required_mappings = {
            "fitness_cost_component": self.fitness_cost_component,
            "fitness_time_component": self.fitness_time_component,
            "fitness_route_component": self.fitness_route_component,
            "coverage_weight": self.coverage_weight,
        }

        for mapping_name, mapping in required_mappings.items():
            missing_variables = variable_set - set(mapping.keys())
            if missing_variables:
                raise MDFHValidationError(
                    f"{mapping_name} is missing values for variables: "
                    f"{sorted(missing_variables)}"
                )

        all_covered_variables: set[str] = set()
        for covered in self.coverage_weight.values():
            all_covered_variables.update(covered)

        unknown_covered_variables = all_covered_variables - variable_set
        if unknown_covered_variables:
            raise MDFHValidationError(
                "coverage_weight contains unknown variables: "
                f"{sorted(unknown_covered_variables)}"
            )
        
    def get_variable_coverage(self, variable: str) -> set[str]:
        """Return the set of variables covered by a given variable.

        Parameters
        ----------
        variable:
            Variable whose coverage set should be returned.

        Returns
        -------
        set[str]
            Variables covered by the given variable.
        """

        if variable not in self.variables:
            raise MDFHValidationError(f"Unknown variable: {variable!r}")

        coverage = set(self.coverage_weight.get(variable, set()))

        if self.include_self:
            coverage.add(variable)

        return coverage

    def get_unassigned_coverage(self, variable: str) -> set[str]:
        """Return candidate variables covered by a given variable."""

        return self.get_variable_coverage(variable) & self.candidate_variables

    def compute_fitness_score(
        self,
        variable: str,
        unassigned_coverage: set[str],
    ) -> float:
        """Compute the multidimensional fitness score for a variable.

        Parameters
        ----------
        variable:
            Candidate variable.

        unassigned_coverage:
            Candidate variables covered by ``variable``.

        Returns
        -------
        float
            Computed multidimensional fitness score.
        """

        sum_cost = sum(
            self.fitness_cost_component[item] for item in unassigned_coverage
        )
        sum_time = sum(
            self.fitness_time_component[item] for item in unassigned_coverage
        )
        sum_route = sum(
            self.fitness_route_component[item] for item in unassigned_coverage
        )

        return (
            sum_cost
            + sum_time
            + sum_route
            - self.fitness_cost_component[variable]
        )

    def solve(self, verbose: bool = False) -> MDFHResult:
        """Solve the set covering problem using the MDFH heuristic.

        Parameters
        ----------
        verbose:
            If True, emit step-by-step logging messages through the logger.

        Returns
        -------
        MDFHResult
            Structured result object containing selected variables, coverage
            information, feasibility, objective value, and runtime.

        Raises
        ------
        MDFHSolverError
            If the solver cannot select a valid candidate variable.
        """

        start_time = time.monotonic()

        if verbose:
            logger.info("Starting MDFH solve process.")

        iteration = 0

        while self.candidate_variables:
            iteration += 1

            best_variable: str | None = None
            best_score = float("-inf")
            best_coverage: set[str] = set()

            for variable in sorted(self.candidate_variables):
                unassigned_coverage = self.get_unassigned_coverage(variable)

                if not unassigned_coverage:
                    continue

                fitness_score = self.compute_fitness_score(
                    variable=variable,
                    unassigned_coverage=unassigned_coverage,
                )

                if fitness_score > best_score:
                    best_score = fitness_score
                    best_variable = variable
                    best_coverage = unassigned_coverage

            if best_variable is None:
                raise MDFHSolverError(
                    "No candidate variable could be selected. "
                    "The problem may be infeasible or the coverage data may be invalid."
                )

            self.y[best_variable] = 1

            if verbose:
                logger.info(
                    "Iteration %d: selected variable=%s, score=%s, covered=%s",
                    iteration,
                    best_variable,
                    best_score,
                    sorted(best_coverage),
                )

            self.candidate_variables -= best_coverage

            for covered_variable in sorted(best_coverage):
                if covered_variable == best_variable:
                    continue

                updated_coverage = self.get_unassigned_coverage(covered_variable)

                if not updated_coverage:
                    self.eliminated_variables.add(covered_variable)
                    self.y[covered_variable] = 0
                    continue

                updated_score = self.compute_fitness_score(
                    variable=covered_variable,
                    unassigned_coverage=updated_coverage,
                )

                if updated_score <= 0:
                    self.eliminated_variables.add(covered_variable)
                    self.y[covered_variable] = 0

                    if verbose:
                        logger.info(
                            "Eliminated variable=%s with updated score=%s",
                            covered_variable,
                            updated_score,
                        )

        objective_value = self._compute_objective_value()
        solve_duration = time.monotonic() - start_time

        result = MDFHResult(
            selected_variables=sorted(self.selected_variables),
            covered_variables=self.covered_variables,
            uncovered_variables=self.uncovered_variables,
            is_feasible=self.is_feasible,
            objective_value=objective_value,
            solve_duration=solve_duration,
        )

        if verbose:
            logger.info(
                "MDFH solve completed. selected=%s, objective=%s, feasible=%s, "
                "duration=%.6f seconds",
                result.selected_variables,
                result.objective_value,
                result.is_feasible,
                result.solve_duration,
            )

        return result

    def _compute_objective_value(self) -> float:
        """Compute objective value for the selected solution.

        The current implementation uses the sum of cost components of selected
        variables as the objective value.
        """

        return sum(
            self.fitness_cost_component[variable]
            for variable in self.selected_variables
        )

    @property
    def selected_variables(self) -> set[str]:
        """Return selected variables."""

        return {
            variable
            for variable, selected in self.y.items()
            if selected == 1
        }

    @property
    def covered_variables(self) -> set[str]:
        """Return all variables covered by selected variables."""

        covered: set[str] = set()

        for variable in self.selected_variables:
            covered.update(self.get_variable_coverage(variable))

        return covered

    @property
    def uncovered_variables(self) -> set[str]:
        """Return variables not covered by the current solution."""

        return set(self.variables) - self.covered_variables

    @property
    def is_feasible(self) -> bool:
        """Return whether all variables are covered."""

        return not self.uncovered_variables
