"""Tests for functions that build calibration solvers."""

from starbox.factory.solver import build_solver
from starbox.calibrate.solver import Solver


def test_build_solver_returns_solver(solver_config):
    """Test that build_solver returns a Solver instance."""
    solver = build_solver(solver_config)

    assert isinstance(solver, Solver)
    assert solver.solint == solver_config.solint
