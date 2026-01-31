"""Tests for the Solver class."""

from starbox.calibrate.solver import Solver
import pytest

from starbox.config.solver import SolverConfig


def test_solver_from_config(solver_config):
    """Test that Solver can be created from SolverConfig."""

    solver = Solver(solver_config)
    assert solver.config.solint == 10


@pytest.mark.parametrize("solint, expected_shape", [(1, (3, 2)), (2, (2, 2))])
def test_solver_solve_method(visibility_set, solint, expected_shape):
    """Test the solve method of the Solver class."""
    solver_config = SolverConfig(solint=solint)
    solver = Solver(solver_config)
    n_stations = 4

    observed_visibilities = visibility_set
    model_visibilities = visibility_set
    solutions = solver.solve(
        observed_visibilities=observed_visibilities,
        model_visibilities=model_visibilities,
        n_stations=n_stations,
    )
    assert solutions.station_phase_gains.shape[0] == expected_shape[0]
    assert solutions.station_phase_gains.shape[1] == expected_shape[1]
    assert solutions.station_phase_gains.shape[2] == n_stations
    assert solutions.station_phase_gains.dtype == "complex64"
