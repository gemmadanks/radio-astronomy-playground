"""Tests for Solutions class."""

import numpy as np

from starbox.calibrate.solutions import Solutions


def test_solutions_initialization(gains):
    """Test that the Solutions class initializes correctly."""
    solutions = Solutions(station_phase_gains=gains)

    assert solutions.station_phase_gains.shape == (3, 2, 4)
    assert solutions.station_phase_gains.dtype == "complex64"


def test_solutions_apply_method(gains, visibility_set):
    """Test the apply method of the Solutions class."""
    solutions = Solutions(station_phase_gains=gains)

    calibrated_visibilities = solutions.apply(visibility_set)

    assert calibrated_visibilities is not visibility_set
    assert calibrated_visibilities.vis.shape == visibility_set.vis.shape
    assert np.array_equal(calibrated_visibilities.station1, visibility_set.station1)
