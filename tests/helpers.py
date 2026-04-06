"""Shared test helpers used across unit and integration test suites."""

import numpy as np

from starbox.visibility import VisibilitySet


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
    """Apply known 1-D per-station phase gains using the project visibility convention."""
    corrupted = _copy_visibility_set(visibility_set)
    gains_1 = station_phase_gains[corrupted.station1][np.newaxis, :, np.newaxis]
    gains_2 = station_phase_gains[corrupted.station2][np.newaxis, :, np.newaxis]
    corrupted.vis *= gains_1 * np.conj(gains_2)
    return corrupted
