"""Tests for Solutions class."""

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

    # Since the apply method is a placeholder, we expect the same object back
    assert calibrated_visibilities is visibility_set
