"""Tests for VisibilitySet"""

import numpy as np
from starbox.visibility import VisibilitySet


def test_visibility_set_creation():
    vis = np.random.randn(10, 5, 6) + 1j * np.random.randn(10, 5, 6)
    uvw_m = np.random.randn(10, 5, 3)
    station1 = np.array([0, 0, 1, 1, 2])
    station2 = np.array([1, 2, 2, 3, 3])
    times_mjd = np.linspace(59000.0, 59000.1, 10)
    freqs_hz = np.array([1e8, 1.1e8, 1.2e8, 1.3e8, 1.4e8, 1.5e8])
    weights = np.ones((10, 5, 6))

    visibility_set = VisibilitySet(
        vis=vis,
        uvw_m=uvw_m,
        station1=station1,
        station2=station2,
        times_mjd=times_mjd,
        freqs_hz=freqs_hz,
        weights=weights,
    )

    assert visibility_set.vis.shape == (10, 5, 6)
    assert visibility_set.uvw_m.shape == (10, 5, 3)
    assert visibility_set.station1.shape == (5,)
    assert visibility_set.station2.shape == (5,)
    assert visibility_set.times_mjd.shape == (10,)
    assert visibility_set.freqs_hz.shape == (6,)
    assert visibility_set.weights.shape == (10, 5, 6)
