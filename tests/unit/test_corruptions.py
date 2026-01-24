"""Tests for Corruptions class."""

import pytest
from starbox.simulate import Corruptions
import numpy as np

from starbox.visibility import VisibilitySet


def test_corruptions_init(corruptions: Corruptions):
    """Test that the Corruptions class initializes correctly."""
    assert corruptions.rms_noise is None
    assert corruptions.station_phase_gain is None
    assert corruptions.sigma is None


def test_corruptions_add_noise(corruptions: Corruptions):
    """Test adding noise to the Corruptions instance."""
    corruptions.add_noise(rms_noise=2.0)
    assert corruptions.rms_noise == 2.0
    assert corruptions.sigma == 2.0 / np.sqrt(2)


@pytest.mark.parametrize("phase_gain", [0.5, 1.0, 3.0, None])
def test_corruptions_add_station_phase_gain(corruptions: Corruptions, phase_gain):
    """Test adding station phase gain to the Corruptions instance."""
    corruptions.add_station_phase_gain(phase_gain)
    assert corruptions.station_phase_gain == phase_gain


def test_corruptions_apply(corruptions: Corruptions, visibility_set: VisibilitySet):
    """Test applying corruptions to visibilities."""

    # Apply without any corruptions
    corrupted_vis = corruptions.apply(visibility_set)
    np.testing.assert_array_equal(corrupted_vis.vis, visibility_set.vis)

    # Add noise and apply
    corruptions.add_noise(rms_noise=0.1)
    corrupted_vis = corruptions.apply(visibility_set)
    assert not np.array_equal(corrupted_vis.vis, visibility_set.vis)

    # Check that the noise level is approximately correct
    noise = corrupted_vis.vis - visibility_set.vis
    measured_rms = np.sqrt(np.mean(np.abs(noise) ** 2))
    assert np.isclose(measured_rms, 0.1, atol=0.05)
