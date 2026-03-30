"""Tests for the Solver class."""

import pytest
import numpy as np

from starbox.calibrate.solver import Solver
from starbox.visibility import VisibilitySet
from starbox.config.solver import SolverConfig


def _copy_visibility_set(visibility_set: VisibilitySet) -> VisibilitySet:
    """Create an isolated copy of a visibility set for test mutation."""

    return VisibilitySet(
        vis=np.array(visibility_set.vis, copy=True),
        uvw_m=np.array(visibility_set.uvw_m, copy=True),
        station1=np.array(visibility_set.station1, copy=True),
        station2=np.array(visibility_set.station2, copy=True),
        times_mjd=np.array(visibility_set.times_mjd, copy=True),
        freqs_hz=np.array(visibility_set.freqs_hz, copy=True),
        weights=np.array(visibility_set.weights, copy=True),
    )


def _apply_station_phase_gains(
    visibility_set: VisibilitySet, station_phase_gains: np.ndarray
) -> VisibilitySet:
    """Apply known station phase gains using the project visibility convention."""

    corrupted = _copy_visibility_set(visibility_set)
    gains_1 = station_phase_gains[corrupted.station1][np.newaxis, :, np.newaxis]
    gains_2 = station_phase_gains[corrupted.station2][np.newaxis, :, np.newaxis]
    corrupted.vis *= gains_1 * np.conj(gains_2)
    return corrupted


def test_solver_from_config(solver_config):
    """Test that Solver can be created from SolverConfig."""

    solver = Solver(solver_config)
    assert solver.config.solution_interval_seconds == 10


@pytest.mark.parametrize(
    "solution_interval_seconds, expected_shape", [(60, (3, 2)), (120, (2, 2))]
)
def test_solver_solve_method_when_model_observed_are_identical(
    visibility_set, solution_interval_seconds, expected_shape
):
    """Test the solve method of the Solver class.

    Checks that the shape and dtype of the station phase gains
    are correct when the observed and model visibilities are identical.
    """
    solver_config = SolverConfig(solution_interval_seconds=solution_interval_seconds)
    solver = Solver(solver_config)
    n_stations = 4

    # Set observed and model visibilities to the same values
    observed_visibilities = _copy_visibility_set(visibility_set)
    model_visibilities = _copy_visibility_set(visibility_set)

    expected_solutions = np.ones(
        (expected_shape[0], expected_shape[1], n_stations),
        dtype=np.complex64,
    )
    # Solve for the station phase gains
    solutions = solver.solve(
        observed_visibilities=observed_visibilities,
        model_visibilities=model_visibilities,
        n_stations=n_stations,
    )

    assert solutions.station_phase_gains.shape[0] == expected_shape[0]
    assert solutions.station_phase_gains.shape[1] == expected_shape[1]
    assert solutions.station_phase_gains.shape[2] == n_stations
    assert solutions.station_phase_gains.dtype == "complex64"
    assert np.allclose(solutions.station_phase_gains, expected_solutions, atol=1e-6)


def test_solver_solve_method_keeps_reference_station_fixed(visibility_set):
    """Test that the solver fixes the reference station to remove phase ambiguity."""

    solver_config = SolverConfig(solution_interval_seconds=60)
    solver = Solver(solver_config)
    n_stations = 4

    model_visibilities = _copy_visibility_set(visibility_set)
    applied_gains = np.array(
        [1.0, np.exp(1j * np.deg2rad(20)), np.exp(1j * np.deg2rad(50)), 1.0],
        dtype=np.complex64,
    )
    observed_visibilities = _apply_station_phase_gains(
        model_visibilities, applied_gains
    )

    solutions = solver.solve(
        observed_visibilities=observed_visibilities,
        model_visibilities=model_visibilities,
        n_stations=n_stations,
    )

    assert np.allclose(solutions.station_phase_gains[..., 0], 1.0 + 0j)


def test_solver_solve_method_leaves_unobserved_stations_at_unity(visibility_set):
    """Test that stations absent from all baselines remain unconstrained at unity."""

    solver_config = SolverConfig(solution_interval_seconds=60)
    solver = Solver(solver_config)
    n_stations = 4

    model_visibilities = _copy_visibility_set(visibility_set)
    applied_gains = np.array(
        [1.0, np.exp(1j * np.deg2rad(15)), np.exp(1j * np.deg2rad(30)), 1.0],
        dtype=np.complex64,
    )
    observed_visibilities = _apply_station_phase_gains(
        model_visibilities, applied_gains
    )

    solutions = solver.solve(
        observed_visibilities=observed_visibilities,
        model_visibilities=model_visibilities,
        n_stations=n_stations,
    )

    assert np.allclose(solutions.station_phase_gains[..., 3], 1.0 + 0j)


@pytest.mark.parametrize("scaling_factor", [0.5, 2])
def test_solver_solve_method_when_model_observed_different(
    visibility_set, scaling_factor
):
    """Test that amplitude-only mismatch is not absorbed by a phase-only solver.

    A phase-only calibration should leave the gains at unity when the only
    difference between observed and model visibilities is a real amplitude scale.
    """
    solver_config = SolverConfig(solution_interval_seconds=60)
    solver = Solver(solver_config)
    n_stations = 4

    observed_visibilities = _copy_visibility_set(visibility_set)
    model_visibilities = _copy_visibility_set(visibility_set)
    model_visibilities.vis *= scaling_factor

    expected_solutions = np.ones(
        (
            observed_visibilities.vis.shape[0],
            observed_visibilities.vis.shape[2],
            n_stations,
        ),
        dtype=np.complex64,
    )

    solutions = solver.solve(
        observed_visibilities=observed_visibilities,
        model_visibilities=model_visibilities,
        n_stations=n_stations,
    )

    assert np.allclose(np.abs(solutions.station_phase_gains), 1.0, atol=1e-6)
    phase_error_1 = np.angle(
        solutions.station_phase_gains[..., 1] * np.conj(expected_solutions[..., 1])
    )
    phase_error_2 = np.angle(
        solutions.station_phase_gains[..., 2] * np.conj(expected_solutions[..., 2])
    )
    assert np.max(np.abs(phase_error_1)) < 1e-6
    assert np.max(np.abs(phase_error_2)) < 1e-6


def test_solver_solve_method_finds_correct_phase_shift(visibility_set):
    """Test that the solve method recovers station phase gains from data.

    The visibility fixture contains baselines 0-1 and 1-2, so with station 0 as the
    reference the recovered gains should form a phase ramp across stations 0, 1, and 2.
    """
    solver_config = SolverConfig(solution_interval_seconds=60)
    solver = Solver(solver_config)
    n_stations = 4

    model_visibilities = _copy_visibility_set(visibility_set)
    angle_rad = np.deg2rad(45)
    applied_gains = np.array(
        [1.0, np.exp(1j * angle_rad), np.exp(2j * angle_rad), 1.0],
        dtype=np.complex64,
    )
    observed_visibilities = _apply_station_phase_gains(
        model_visibilities, applied_gains
    )

    expected_solutions = np.ones(
        (
            observed_visibilities.vis.shape[0],
            observed_visibilities.vis.shape[2],
            n_stations,
        ),
        dtype=np.complex64,
    )
    expected_solutions *= applied_gains[np.newaxis, np.newaxis, :]

    solutions = solver.solve(
        observed_visibilities=observed_visibilities,
        model_visibilities=model_visibilities,
        n_stations=n_stations,
    )

    assert np.allclose(np.abs(solutions.station_phase_gains), 1.0, atol=1e-6)
    phase_error_1 = np.angle(
        solutions.station_phase_gains[..., 1] * np.conj(expected_solutions[..., 1])
    )
    phase_error_2 = np.angle(
        solutions.station_phase_gains[..., 2] * np.conj(expected_solutions[..., 2])
    )
    assert np.max(np.abs(phase_error_1)) < 1e-6
    assert np.max(np.abs(phase_error_2)) < 1e-6


@pytest.mark.parametrize("scaling_factor", [0.5, 2.0])
def test_solver_solve_method_returns_unit_modulus_gains(visibility_set, scaling_factor):
    """Test that solved gains stay on the unit circle for phase-only calibration."""

    solver_config = SolverConfig(solution_interval_seconds=60)
    solver = Solver(solver_config)

    observed_visibilities = _copy_visibility_set(visibility_set)
    model_visibilities = _copy_visibility_set(visibility_set)
    model_visibilities.vis *= scaling_factor

    solutions = solver.solve(
        observed_visibilities=observed_visibilities,
        model_visibilities=model_visibilities,
        n_stations=4,
    )

    assert np.allclose(np.abs(solutions.station_phase_gains), 1.0, atol=1e-6)


@pytest.mark.parametrize("phase_shift", [0.0, np.deg2rad(30), np.deg2rad(60)])
def test_solver_residuals_method(visibility_set, phase_shift):
    """Test residuals for correct and incorrect phase-only gain solutions.

    Residuals should be zero when the supplied gains reproduce the observed data,
    and non-zero when they do not.
    """
    solver_config = SolverConfig(solution_interval_seconds=60)
    solver = Solver(solver_config)

    model_visibilities = _copy_visibility_set(visibility_set)
    n_stations = 4
    station_gains = np.array(
        [1.0, np.exp(1j * phase_shift), np.exp(2j * phase_shift), 1.0],
        dtype=np.complex64,
    )
    observed_visibilities = _apply_station_phase_gains(
        model_visibilities, station_gains
    )
    n_time_bins = observed_visibilities.vis.shape[0]
    n_freq_bins = observed_visibilities.vis.shape[2]
    gains = np.ones((n_time_bins, n_freq_bins, n_stations), dtype=np.complex64)
    gains *= station_gains[np.newaxis, np.newaxis, :]

    residuals = solver._residuals(gains, observed_visibilities, model_visibilities)

    assert np.allclose(residuals, 0.0, atol=1e-6)

    incorrect_gains = np.ones(
        (n_time_bins, n_freq_bins, n_stations), dtype=np.complex64
    )
    incorrect_residuals = solver._residuals(
        incorrect_gains, observed_visibilities, model_visibilities
    )
    if phase_shift == 0.0:
        assert np.allclose(incorrect_residuals, 0.0, atol=1e-6)
    else:
        assert not np.allclose(incorrect_residuals, 0.0, atol=1e-6)


def test_solver_residuals_method_returns_real_finite_vector(visibility_set):
    """Test that residuals satisfy the SciPy least-squares interface contract."""

    solver_config = SolverConfig(solution_interval_seconds=60)
    solver = Solver(solver_config)

    observed_visibilities = _copy_visibility_set(visibility_set)
    model_visibilities = _copy_visibility_set(visibility_set)
    gains = np.ones((3, 2, 4), dtype=np.complex64)

    residuals = solver._residuals(gains, observed_visibilities, model_visibilities)

    assert residuals.ndim == 1
    assert np.isrealobj(residuals)
    assert np.all(np.isfinite(residuals))


def test_solver_residuals_method_accepts_1d_real_phase_vector(visibility_set):
    """Test the SciPy calling path: _residuals accepts a 1D real phase vector."""

    solver_config = SolverConfig(solution_interval_seconds=60)
    solver = Solver(solver_config)
    n_stations = 4
    n_time_bins = visibility_set.vis.shape[0]  # 3
    n_freq_bins = visibility_set.vis.shape[2]  # 2

    observed_visibilities = _copy_visibility_set(visibility_set)
    model_visibilities = _copy_visibility_set(visibility_set)

    # Zero phase vector → all gains = 1+0j → residuals should be zero for identical visibilities
    phases = np.zeros(n_time_bins * n_freq_bins * (n_stations - 1))

    residuals = solver._residuals(
        phases, observed_visibilities, model_visibilities, n_stations=n_stations
    )

    assert residuals.ndim == 1
    assert np.isrealobj(residuals)
    assert np.all(np.isfinite(residuals))
    assert np.allclose(residuals, 0.0, atol=1e-6)


def test_solver_residuals_method_scales_by_weights(visibility_set):
    """Test that residuals are scaled by sqrt(weights)."""

    solver_config = SolverConfig(solution_interval_seconds=60)
    solver = Solver(solver_config)

    model_visibilities = _copy_visibility_set(visibility_set)
    station_gains = np.array(
        [1.0, np.exp(1j * np.deg2rad(30)), np.exp(2j * np.deg2rad(30)), 1.0],
        dtype=np.complex64,
    )
    observed_visibilities = _apply_station_phase_gains(
        model_visibilities, station_gains
    )

    n_time_bins = observed_visibilities.vis.shape[0]
    n_freq_bins = observed_visibilities.vis.shape[2]
    n_stations = 4
    unity_gains = np.ones((n_time_bins, n_freq_bins, n_stations), dtype=np.complex64)

    residuals_unit = solver._residuals(
        unity_gains, observed_visibilities, model_visibilities
    )

    double_weight_observed = _copy_visibility_set(observed_visibilities)
    double_weight_observed.weights *= 2.0
    residuals_double = solver._residuals(
        unity_gains, double_weight_observed, model_visibilities
    )

    assert np.allclose(residuals_double, residuals_unit * np.sqrt(2.0), atol=1e-6)


def test_solver_uses_timestamps_to_define_solution_bins(visibility_set):
    """Test solver bins by elapsed seconds, not by sample index."""

    solver = Solver(SolverConfig(solution_interval_seconds=60))

    solutions = solver.solve(
        observed_visibilities=_copy_visibility_set(visibility_set),
        model_visibilities=_copy_visibility_set(visibility_set),
        n_stations=4,
    )

    assert solutions.station_phase_gains.shape == (3, 2, 4)

    solver = Solver(SolverConfig(solution_interval_seconds=120))

    solutions = solver.solve(
        observed_visibilities=_copy_visibility_set(visibility_set),
        model_visibilities=_copy_visibility_set(visibility_set),
        n_stations=4,
    )

    assert solutions.station_phase_gains.shape == (2, 2, 4)


# ---------------------------------------------------------------------------
# _phases_to_gains
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "n_time_bins, n_freq_bins, n_stations",
    [(1, 1, 2), (3, 2, 4), (2, 3, 5)],
)
def test_phases_to_gains_output_shape(n_time_bins, n_freq_bins, n_stations):
    """Test that _phases_to_gains returns an array of the correct shape."""

    solver = Solver(SolverConfig(solution_interval_seconds=1))
    phases = np.zeros(n_time_bins * n_freq_bins * (n_stations - 1))

    gains = solver._phases_to_gains(phases, n_time_bins, n_freq_bins, n_stations)

    assert gains.shape == (n_time_bins, n_freq_bins, n_stations)


def test_phases_to_gains_reference_station_is_unity(visibility_set):
    """Test that _phases_to_gains always pins station 0 to 1+0j."""

    solver = Solver(SolverConfig(solution_interval_seconds=1))
    n_time_bins, n_freq_bins, n_stations = 3, 2, 4
    phases = np.random.default_rng(42).uniform(
        -np.pi, np.pi, n_time_bins * n_freq_bins * (n_stations - 1)
    )

    gains = solver._phases_to_gains(phases, n_time_bins, n_freq_bins, n_stations)

    assert np.allclose(gains[:, :, 0], 1.0 + 0j)


def test_phases_to_gains_produces_unit_modulus_gains():
    """Test that all gains returned by _phases_to_gains lie on the unit circle."""

    solver = Solver(SolverConfig(solution_interval_seconds=1))
    n_time_bins, n_freq_bins, n_stations = 3, 2, 4
    phases = np.random.default_rng(7).uniform(
        -np.pi, np.pi, n_time_bins * n_freq_bins * (n_stations - 1)
    )

    gains = solver._phases_to_gains(phases, n_time_bins, n_freq_bins, n_stations)

    assert np.allclose(np.abs(gains), 1.0, atol=1e-6)


@pytest.mark.parametrize(
    "phase_rad", [0.0, np.deg2rad(45), np.deg2rad(90), np.deg2rad(180)]
)
def test_phases_to_gains_maps_known_phase_correctly(phase_rad):
    """Test that a single known phase maps to the expected complex gain."""

    solver = Solver(SolverConfig(solution_interval_seconds=1))
    # 1 time bin, 1 freq bin, 2 stations (only station 1 is free)
    phases = np.array([phase_rad])

    gains = solver._phases_to_gains(phases, n_time_bins=1, n_freq_bins=1, n_stations=2)

    assert np.isclose(gains[0, 0, 0], 1.0 + 0j)
    assert np.isclose(gains[0, 0, 1], np.exp(1j * phase_rad))
