"""Tests for Corruptions class."""

import pytest
from starbox.simulate import Corruptions
import numpy as np

from starbox.visibility import VisibilitySet


def test_corruptions_from_spec(corruptions_spec):
    """Test that Corruptions can be created from CorruptionsSpec."""
    corruptions = Corruptions.from_spec(corruptions_spec)

    assert corruptions.seed == 42
    assert corruptions.rms_noise == 1.0
    assert corruptions.rms_phase_gain == 2.0
    assert corruptions.sigma == 1.0 / np.sqrt(2)


def test_corruptions_init(corruptions):
    """Test that the Corruptions class initializes correctly."""
    assert corruptions.rms_noise is None
    assert corruptions.rms_phase_gain is None
    assert corruptions.sigma is None


def test_corruptions_add_noise(corruptions: Corruptions):
    """Test adding noise to the Corruptions instance."""
    corruptions._add_noise(rms_noise=2.0)
    assert corruptions.rms_noise == 2.0
    assert corruptions.sigma == 2.0 / np.sqrt(2)


@pytest.mark.parametrize("phase_gain", [0.5, 1.0, 3.0, None])
def test_corruptions_add_station_phase_gain(corruptions: Corruptions, phase_gain):
    """Test adding station phase gain to the Corruptions instance."""
    corruptions.add_station_phase_gain(phase_gain)
    assert corruptions.rms_phase_gain == phase_gain


def test_corruptions_apply_noise(
    corruptions: Corruptions, visibility_set: VisibilitySet
):
    """Test applying corruptions to visibilities."""

    # Apply without any corruptions
    corrupted_vis = corruptions.apply(visibility_set)
    np.testing.assert_array_equal(corrupted_vis.vis, visibility_set.vis)

    # Add noise and apply
    corruptions._add_noise(rms_noise=0.1)
    corrupted_vis = corruptions.apply(visibility_set)
    assert not np.array_equal(corrupted_vis.vis, visibility_set.vis)

    # Check that the noise level is approximately correct
    noise = corrupted_vis.vis - visibility_set.vis
    measured_rms = np.sqrt(np.mean(np.abs(noise) ** 2))
    assert np.isclose(measured_rms, 0.1, atol=0.05)


def test_apply_without_rms_phase_gain(
    corruptions: Corruptions, visibility_set: VisibilitySet, mocker
):
    """Test that applying corruptions without setting rms phase."""
    spy_sample_station_phase_gains = mocker.spy(
        Corruptions, "_sample_station_phase_gains"
    )
    spy_apply_station_phase_gain = mocker.spy(Corruptions, "_apply_station_phase_gain")
    _ = corruptions.apply(visibility_set)
    spy_sample_station_phase_gains.assert_not_called()
    spy_apply_station_phase_gain.assert_not_called()


def test_apply_without_rms_noise(
    corruptions: Corruptions, visibility_set: VisibilitySet, mocker
):
    """Test that applying corruptions without setting rms noise."""
    spy_apply_noise = mocker.spy(Corruptions, "_apply_noise")
    _ = corruptions.apply(visibility_set)
    spy_apply_noise.assert_not_called()


def test_apply_noise_without_sigma_raises(
    corruptions: Corruptions, visibility_set: VisibilitySet
):
    """Test that applying noise without setting sigma raises an error."""
    with pytest.raises(ValueError, match="Sigma for noise is not set."):
        corruptions._apply_noise(visibility_set)


def test_corruptions_apply_station_phase_gain(
    corruptions: Corruptions, visibility_set: VisibilitySet
):
    """Test applying station phase gain corruptions to visibilities."""
    corrupted_vis = VisibilitySet(
        vis=np.copy(visibility_set.vis),
        uvw_m=visibility_set.uvw_m,
        station1=visibility_set.station1,
        station2=visibility_set.station2,
        times_mjd=visibility_set.times_mjd,
        freqs_hz=visibility_set.freqs_hz,
        weights=visibility_set.weights,
    )
    # Add station random phase gain and apply
    phase_gain_station0 = np.exp(1j * 0)  # 0 degree phase shift (reference)
    phase_gain_station1 = np.exp(1j * np.pi / 4)  # 45 degree phase shift
    phase_gain_station2 = np.exp(1j * np.pi / 2)  # 90 degree phase shift
    phase_gain = np.array(
        [phase_gain_station0, phase_gain_station1, phase_gain_station2]
    )
    corrupted_vis = corruptions._apply_station_phase_gain(corrupted_vis, phase_gain)

    assert not np.array_equal(corrupted_vis.vis, visibility_set.vis)
    # Check that the phase gains have been applied correctly
    assert np.allclose(
        corrupted_vis.vis[0, 0, 0], phase_gain_station0 * np.conj(phase_gain_station1)
    )
    assert np.allclose(
        corrupted_vis.vis[0, 1, 0], phase_gain_station1 * np.conj(phase_gain_station2)
    )


def test_corruptions_sample_station_phase_gains(corruptions: Corruptions):
    """Test sampling of station phase gains."""
    corruptions.add_station_phase_gain(rms_phase_gain=0.5)
    num_stations = 5
    phase_gains = corruptions._sample_station_phase_gains(num_stations)

    assert phase_gains.shape == (num_stations,)
    # Check that the reference station has zero phase gain
    assert np.isclose(phase_gains[0], 1.0 + 0j)


def test_corruptions_sample_station_phase_gains_no_rms(corruptions: Corruptions):
    """Test that sampling station phase gains without setting rms raises an error."""
    num_stations = 5
    with pytest.raises(ValueError, match="RMS phase gain is not set."):
        corruptions._sample_station_phase_gains(num_stations)


def test_corruptions_apply_with_station_phase_gain(
    corruptions: Corruptions, visibility_set: VisibilitySet
):
    """Test applying corruptions with station phase gain set."""
    corruptions.add_station_phase_gain(rms_phase_gain=0.5)
    corrupted_vis = corruptions.apply(visibility_set)

    assert not np.array_equal(corrupted_vis.vis, visibility_set.vis)
