"""Functions to build calibration solvers."""

from starbox.calibrate.solver import Solver
from starbox.config.solver import SolverConfig


def build_solver(cfg: SolverConfig) -> Solver:
    """Build a Solver instance from the given configuration.

    Args:
        cfg: Configuration for the solver.
    Returns:
        An instance of Solver.
    """
    return Solver(cfg)
