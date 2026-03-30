"""Integration tests for the calibration pipeline (corrupt → solve → apply)."""

import numpy as np
import pytest

from starbox.calibrate.solver import Solver
from starbox.config.corruptions import CorruptionsConfig
from starbox.config.solver import SolverConfig
from starbox.simulate.corruptions import Corruptions
from tests.helpers import _copy_visibility_set


@pytest.mark.parametrize(
    "phase_deg_station1, phase_deg_station2",
    [
        (30.0, 60.0),
        (45.0, -45.0),
        (0.0, 90.0),
    ],
)
def test_solver_end_to_end_corrected_visibilities_closer_to_model(
    visibility_set, phase_deg_station1, phase_deg_station2
):
    """End-to-end: corrupt → solve → apply produces visibilities closer to the model.

    This is the fundamental correctness test for the calibration pipeline.
    Given noise-free data corrupted by known per-station phase gains, the
    corrected visibilities must be closer to the model than the corrupted ones.
    """
    solver = Solver(SolverConfig(solution_interval_seconds=60))
    n_stations = 4

    model_visibilities = _copy_visibility_set(visibility_set)

    # Build exact known gains and corrupt using the production Corruptions method.
    true_gains = np.array(
        [
            1.0,
            np.exp(1j * np.deg2rad(phase_deg_station1)),
            np.exp(1j * np.deg2rad(phase_deg_station2)),
            1.0,
        ],
        dtype=np.complex64,
    )
    corruptions = Corruptions(
        CorruptionsConfig(seed=42, rms_noise=0.0, rms_phase_gain=0.0)
    )
    observed_visibilities = corruptions._apply_station_phase_gain(
        _copy_visibility_set(model_visibilities), true_gains
    )

    solutions = solver.solve(
        observed_visibilities=observed_visibilities,
        model_visibilities=model_visibilities,
        n_stations=n_stations,
    )
    corrected_visibilities = solutions.apply(observed_visibilities)

    error_before = np.mean(
        np.abs(observed_visibilities.vis - model_visibilities.vis) ** 2
    )
    error_after = np.mean(
        np.abs(corrected_visibilities.vis - model_visibilities.vis) ** 2
    )

    assert error_after < error_before, (
        f"Calibration made things worse: MSE before={error_before:.6f}, after={error_after:.6f}"
    )
