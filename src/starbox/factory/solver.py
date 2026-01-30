"""Functions to build calibration solvers."""

from starbox.calibrate.solver import Solver, SolverSpec


def build_solver(cfg: SolverSpec) -> Solver:
    """Build a Solver instance from the given configuration.

    Args:
        solver_config: Configuration for the solver.
    Returns:
        An instance of Solver.
    """
    spec = SolverSpec(**cfg.model_dump())
    return Solver.from_spec(spec)
