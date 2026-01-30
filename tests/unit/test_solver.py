"""Tests for the Solver class."""

from starbox.calibrate.solver import Solver
import pytest


def test_solver_initialization():
    """Test that the Solver initializes correctly."""
    solver = Solver(solint=10)
    assert solver.solint == 10


def test_solver_invalid_solint():
    """Test that the Solver raises error for invalid solint."""
    with pytest.raises(ValueError, match="Solution interval must be positive."):
        Solver(solint=0)
    with pytest.raises(ValueError, match="Solution interval must be positive."):
        Solver(solint=-5)


def test_solver_from_spec(solver_spec):
    """Test that Solver can be created from SolverSpec."""

    solver = Solver.from_spec(solver_spec)
    assert solver.solint == 10


@pytest.mark.parametrize("solint, expected_shape", [(1, (3, 2)), (2, (2, 2))])
def test_solver_solve_method(visibility_set, solint, expected_shape):
    """Test the solve method of the Solver class."""
    solver = Solver(solint=solint)
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
