"""Tests for Corruptions class."""

import pytest
from starbox.config.corruptions import CorruptionsConfig
from starbox.simulate import Corruptions
import numpy as np

from starbox.visibility import VisibilitySet


@pytest.mark.parametrize(
    "seed,rms_noise,rms_phase_gain",
    [
        (42, 1.0, 0.5),
        (123, 0.1, 1.0),
        (999, 0.0, 0.0),
    ],
)
def test_corruptions_initialisation(seed, rms_noise, rms_phase_gain):
    """Test adding noise to the Corruptions instance."""
    corruptions_config = CorruptionsConfig(
        seed=seed,
        rms_noise=rms_noise,
        rms_phase_gain=rms_phase_gain,
    )
    corruptions = Corruptions(corruptions_config)
    assert corruptions.config.rms_noise == rms_noise
    assert corruptions.sigma == rms_noise / np.sqrt(2)
    assert corruptions.config.rms_phase_gain == rms_phase_gain


def test_corruptions_apply_no_noise_no_phase_gain(visibility_set: VisibilitySet):
    """Test applying corruptions with no noise and no phase gain set."""
    corruptions_config = CorruptionsConfig(
        seed=42,
        rms_noise=0.0,
        rms_phase_gain=0.0,
    )
    corruptions = Corruptions(corruptions_config)
    corrupted_vis = corruptions.apply(visibility_set)
    np.testing.assert_array_equal(corrupted_vis.vis, visibility_set.vis)


def test_corruptions_apply_with_only_noise(mocker, visibility_set: VisibilitySet):
    """Test applying noise-only corruptions to visibilities."""
    corruptions_config = CorruptionsConfig(
        seed=42,
        rms_noise=0.1,
        rms_phase_gain=0.0,
    )
    corruptions = Corruptions(corruptions_config)

    corrupted_vis = corruptions.apply(visibility_set)
    assert not np.array_equal(corrupted_vis.vis, visibility_set.vis)

    # Check that the noise level is approximately correct
    noise = corrupted_vis.vis - visibility_set.vis
    measured_rms = np.sqrt(np.mean(np.abs(noise) ** 2))
    assert np.isclose(measured_rms, 0.1, atol=0.05)


def test_apply_with_only_station_phase_gains(visibility_set: VisibilitySet, mocker):
    """Test that applying corruptions without setting rms noise."""
    corruptions_config = CorruptionsConfig(
        seed=42,
        rms_noise=0.0,
        rms_phase_gain=0.5,
    )
    corruptions = Corruptions(corruptions_config)
    corrupted_vis = corruptions.apply(visibility_set)

    assert not np.array_equal(corrupted_vis.vis, visibility_set.vis)


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
    config = CorruptionsConfig(
        seed=42,
        rms_noise=1.0,
        rms_phase_gain=0.5,
    )
    corruptions = Corruptions(config)
    corruptions._add_station_phase_gain()
    num_times = 3
    num_channels = 2
    num_stations = 5
    phase_gains = corruptions._sample_station_phase_gains(
        num_times=num_times,
        num_channels=num_channels,
        num_stations=num_stations,
    )

    assert phase_gains.shape == (num_times, num_channels, num_stations)
    # Check that the reference station has zero phase gain
    assert np.allclose(phase_gains[..., 0], 1.0 + 0j)


def test_corruptions_sample_station_phase_gains_rms_is_in_degrees():
    """Test that rms_phase_gain is interpreted as degrees, not radians.

    With rms_phase_gain=2 degrees, the standard deviation of extracted phase
    angles must be close to 2 degrees, not 2 radians (~115 degrees).
    """
    config = CorruptionsConfig(seed=42, rms_noise=0.0, rms_phase_gain=2.0)
    corruptions = Corruptions(config)
    phase_gains = corruptions._sample_station_phase_gains(
        num_times=500, num_channels=10, num_stations=10
    )
    # Exclude reference station (index 0 is always 1+0j)
    angles_deg = np.angle(phase_gains[..., 1:], deg=True)
    measured_rms = np.sqrt(np.mean(angles_deg**2))
    assert (
        measured_rms < 10.0
    ), f"Phase RMS is {measured_rms:.1f} deg — rms_phase_gain may be in radians"
    assert np.isclose(
        measured_rms, 2.0, atol=0.5
    ), f"Expected phase RMS ~2 deg, got {measured_rms:.2f} deg"


def test_corruptions_sample_station_phase_gains_vary_over_time_and_frequency():
    """Test sampled station gains are not constant over time/frequency."""

    config = CorruptionsConfig(
        seed=42,
        rms_noise=0.0,
        rms_phase_gain=0.5,
    )
    corruptions = Corruptions(config)

    phase_gains = corruptions._sample_station_phase_gains(
        num_times=3,
        num_channels=2,
        num_stations=5,
    )

    assert not np.allclose(phase_gains[0, :, 1:], phase_gains[1, :, 1:])
    assert not np.allclose(phase_gains[:, 0, 1:], phase_gains[:, 1, 1:])


def test_corruptions_apply_with_station_phase_gain(
    corruptions: Corruptions, visibility_set: VisibilitySet
):
    """Test applying corruptions with station phase gain set."""
    corruptions._add_station_phase_gain()
    corrupted_vis = corruptions.apply(visibility_set)

    assert not np.array_equal(corrupted_vis.vis, visibility_set.vis)


def test_corruptions_apply_phase_gain_varies_across_time_and_frequency(
    visibility_set: VisibilitySet,
):
    """Test applied phase gains affect different time/frequency samples differently."""

    corruptions = Corruptions(
        CorruptionsConfig(seed=42, rms_noise=0.0, rms_phase_gain=0.5)
    )

    corrupted_vis = corruptions.apply(visibility_set)

    ratios = corrupted_vis.vis / visibility_set.vis
    assert not np.allclose(ratios[0, :, :], ratios[1, :, :])
    assert not np.allclose(ratios[:, :, 0], ratios[:, :, 1])


def test_corruptions_sample_station_phase_gains_are_time_correlated():
    """Sampled phases should be correlated along time for realistic drifts."""

    config = CorruptionsConfig(
        seed=7,
        rms_noise=0.0,
        rms_phase_gain=3.0,
        phase_time_correlation=0.98,
        phase_frequency_correlation=0.0,
    )
    corruptions = Corruptions(config)

    phase_gains = corruptions._sample_station_phase_gains(
        num_times=200,
        num_channels=8,
        num_stations=5,
    )
    phases_deg = np.angle(phase_gains[..., 1], deg=True)
    corr_t = np.corrcoef(phases_deg[1:, :].ravel(), phases_deg[:-1, :].ravel())[0, 1]

    assert corr_t > 0.6


def test_corruptions_sample_station_phase_gains_are_frequency_correlated():
    """Sampled phases should be correlated across neighboring channels."""

    config = CorruptionsConfig(
        seed=11,
        rms_noise=0.0,
        rms_phase_gain=3.0,
        phase_time_correlation=0.0,
        phase_frequency_correlation=0.98,
    )
    corruptions = Corruptions(config)

    phase_gains = corruptions._sample_station_phase_gains(
        num_times=80,
        num_channels=64,
        num_stations=5,
    )
    phases_deg = np.angle(phase_gains[..., 1], deg=True)
    corr_f = np.corrcoef(phases_deg[:, 1:].ravel(), phases_deg[:, :-1].ravel())[0, 1]

    assert corr_f > 0.6


# ---------------------------------------------------------------------------
# AR(1) filter edge cases
# ---------------------------------------------------------------------------


def test_corruptions_apply_ar1_with_single_sample():
    """Test AR(1) filter returns unchanged array when axis dimension is 1."""

    samples = np.array([[[1.0, 2.0, 3.0]]])  # Shape (1, 1, 3)
    rho = 0.95
    axis = 0

    result = Corruptions._apply_ar1(samples, rho, axis)

    assert result.shape == samples.shape
    assert np.allclose(result, samples)


def test_corruptions_apply_ar1_with_zero_correlation():
    """Test AR(1) filter with rho=0 returns independent samples (white noise path)."""

    samples = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])  # Shape (3, 2)
    rho = 0.0
    axis = 0

    result = Corruptions._apply_ar1(samples, rho, axis)

    # With rho=0, samples should be unchanged
    assert np.allclose(result, samples)


def test_corruptions_apply_ar1_preserves_shape():
    """Test that AR(1) filter preserves input array shape."""

    samples = np.random.randn(10, 5, 3).astype(np.float32)
    rho = 0.8

    for axis in [0, 1, 2]:
        result = Corruptions._apply_ar1(samples, rho, axis)
        assert result.shape == samples.shape
        assert result.dtype == samples.dtype


def test_corruptions_apply_ar1_high_correlation():
    """Test AR(1) filter produces correlated output when rho is high."""

    np.random.seed(42)
    samples = np.random.randn(100)
    rho = 0.95

    result = Corruptions._apply_ar1(samples, rho, axis=0)

    # With high rho, output should be highly correlated with itself shifted
    lag1_corr = np.corrcoef(result[1:], result[:-1])[0, 1]
    assert lag1_corr > 0.8


def test_corruptions_sample_phase_gains_with_single_time(corruptions_config):
    """Test phase gain sampling with num_times=1."""

    corruptions = Corruptions(corruptions_config)

    phase_gains = corruptions._sample_station_phase_gains(
        num_times=1,
        num_channels=4,
        num_stations=3,
    )

    assert phase_gains.shape == (1, 4, 3)
    assert np.isclose(np.abs(phase_gains[0, :, 0]), 1.0).all()  # Reference station
    assert np.allclose(np.abs(phase_gains[..., 1:]), 1.0, atol=1e-6)  # Unit modulus


def test_corruptions_sample_phase_gains_with_single_channel(corruptions_config):
    """Test phase gain sampling with num_channels=1."""

    corruptions = Corruptions(corruptions_config)

    phase_gains = corruptions._sample_station_phase_gains(
        num_times=10,
        num_channels=1,
        num_stations=3,
    )

    assert phase_gains.shape == (10, 1, 3)
    assert np.isclose(np.abs(phase_gains[:, 0, 0]), 1.0).all()  # Reference station
    assert np.allclose(np.abs(phase_gains[..., 1:]), 1.0, atol=1e-6)  # Unit modulus
