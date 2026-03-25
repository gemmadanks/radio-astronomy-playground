"""Tests for Solutions class."""

import numpy as np

from starbox.calibrate.solutions import Solutions
from starbox.visibility import VisibilitySet


def test_solutions_initialization(gains):
    """Test that the Solutions class initializes correctly."""
    solutions = Solutions(station_phase_gains=gains)

    assert solutions.station_phase_gains.shape == (3, 2, 4)
    assert solutions.station_phase_gains.dtype == "complex64"


def test_solutions_apply_method(gains, visibility_set):
    """Test that apply removes known phase corruptions from visibilities."""
    del gains  # this test builds deterministic gains for a known expected output

    model_vis = np.array(visibility_set.vis, copy=True)
    station_gains = np.array(
        [
            [
                [
                    1.0 + 0j,
                    np.exp(1j * np.deg2rad(20)),
                    np.exp(1j * np.deg2rad(50)),
                    1.0 + 0j,
                ],
                [
                    1.0 + 0j,
                    np.exp(1j * np.deg2rad(25)),
                    np.exp(1j * np.deg2rad(55)),
                    1.0 + 0j,
                ],
            ]
        ]
        * visibility_set.vis.shape[0],
        dtype=np.complex64,
    )

    g1 = np.transpose(station_gains[:, :, visibility_set.station1], (0, 2, 1))
    g2 = np.transpose(station_gains[:, :, visibility_set.station2], (0, 2, 1))
    corrupted_vis = model_vis * (g1 * np.conj(g2))

    corrupted = VisibilitySet(
        vis=corrupted_vis,
        uvw_m=np.array(visibility_set.uvw_m, copy=True),
        station1=np.array(visibility_set.station1, copy=True),
        station2=np.array(visibility_set.station2, copy=True),
        times_mjd=np.array(visibility_set.times_mjd, copy=True),
        freqs_hz=np.array(visibility_set.freqs_hz, copy=True),
        weights=np.array(visibility_set.weights, copy=True),
    )

    solutions = Solutions(station_phase_gains=station_gains)
    calibrated_visibilities = solutions.apply(corrupted)

    assert np.allclose(calibrated_visibilities.vis, model_vis, atol=1e-6)
    assert calibrated_visibilities.vis.shape == visibility_set.vis.shape
    assert calibrated_visibilities.vis.dtype == visibility_set.vis.dtype
    assert np.array_equal(calibrated_visibilities.station1, visibility_set.station1)
    assert np.array_equal(calibrated_visibilities.station2, visibility_set.station2)
    assert np.array_equal(calibrated_visibilities.times_mjd, visibility_set.times_mjd)
    assert np.array_equal(calibrated_visibilities.freqs_hz, visibility_set.freqs_hz)


def test_solutions_apply_method_with_unity_gains_is_identity(visibility_set):
    """Applying unity gains should leave visibilities unchanged."""

    n_times, _, n_channels = visibility_set.vis.shape
    n_stations = 4
    unity_gains = np.ones((n_times, n_channels, n_stations), dtype=np.complex64)
    solutions = Solutions(station_phase_gains=unity_gains)

    calibrated = solutions.apply(visibility_set)

    assert np.allclose(calibrated.vis, visibility_set.vis)


def test_solutions_apply_method_returns_new_visibility_set_instance(visibility_set):
    """Apply should return a new VisibilitySet and not mutate the input object."""

    n_times, _, n_channels = visibility_set.vis.shape
    n_stations = 4
    unity_gains = np.ones((n_times, n_channels, n_stations), dtype=np.complex64)
    solutions = Solutions(station_phase_gains=unity_gains)

    input_vis_copy = np.array(visibility_set.vis, copy=True)
    calibrated = solutions.apply(visibility_set)

    assert calibrated is not visibility_set
    assert np.array_equal(visibility_set.vis, input_vis_copy)


def test_solutions_apply_method_maps_time_and_frequency_bins(visibility_set):
    """Apply should correctly map visibility axes onto coarser solution bins."""

    # Visibility fixture is (3 times, 2 channels); use (2 time bins, 1 freq bin)
    n_stations = 4
    station_gains = np.array(
        [
            [[1.0 + 0j, np.exp(1j * 0.2), np.exp(1j * 0.4), 1.0 + 0j]],
            [[1.0 + 0j, np.exp(1j * 0.6), np.exp(1j * 0.8), 1.0 + 0j]],
        ],
        dtype=np.complex64,
    )

    model_vis = np.array(visibility_set.vis, copy=True)

    # Expected mapping by implementation:
    # time_idx for n_times=3 and n_time_bins=2 -> [0, 0, 1]
    time_idx = np.array([0, 0, 1])
    g_time = station_gains[time_idx, 0, :]
    g1 = g_time[:, visibility_set.station1][:, :, np.newaxis]
    g2 = g_time[:, visibility_set.station2][:, :, np.newaxis]
    corrupted_vis = model_vis * (g1 * np.conj(g2))

    corrupted = VisibilitySet(
        vis=corrupted_vis,
        uvw_m=np.array(visibility_set.uvw_m, copy=True),
        station1=np.array(visibility_set.station1, copy=True),
        station2=np.array(visibility_set.station2, copy=True),
        times_mjd=np.array(visibility_set.times_mjd, copy=True),
        freqs_hz=np.array(visibility_set.freqs_hz, copy=True),
        weights=np.array(visibility_set.weights, copy=True),
    )

    solutions = Solutions(station_phase_gains=station_gains)
    calibrated = solutions.apply(corrupted)

    assert np.allclose(calibrated.vis, model_vis, atol=1e-6)
