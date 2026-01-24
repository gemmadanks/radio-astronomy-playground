"""Tests for Solutions class."""

from starbox.calibrate.solutions import Solutions
import numpy as np
import pytest


def test_solutions_initialization(gains):
    """Test that the Solutions class initializes correctly."""
    solutions = Solutions(gains=gains)

    assert solutions.gains.shape == (3, 2, 4)
    assert solutions.gains.dtype == "complex64"


def test_solutions_apply_method(gains, visibility_set):
    """Test the apply method of the Solutions class."""
    solutions = Solutions(gains=gains)

    calibrated_visibilities = solutions.apply(visibility_set)

    # Since the apply method is a placeholder, we expect the same object back
    assert calibrated_visibilities is visibility_set
