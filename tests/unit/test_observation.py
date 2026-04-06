"""Tests for Observation class."""

from types import SimpleNamespace

from astropy.time import Time
from astropy.utils import iers
from starbox.config.observation import ObservationConfig
from starbox.simulate import Observation
from starbox.geometry.uvw import calculate_uvw
import numpy as np
import math


def test_observation_from_config(observation_config):
    """Test that Observation can be created from ObservationConfig."""

    observation = Observation(observation_config)

    assert observation.config == observation_config
    assert observation.channel_width == (
        observation_config.total_bandwidth / observation_config.num_channels
    )
    assert observation.times_mjd is not None
    assert observation.frequencies_hz is not None


def test_observation_times(observation: Observation):
    """Test that the times property generates correct time steps."""

    # Compute expected times based on the observation config
    n_steps = observation.config.num_timesteps
    if n_steps > 1:
        timestep_mjd = observation.config.observation_length / (n_steps - 1) / 86_400.0
        expected_times = np.array([
            observation.config.start_time_mjd + i * timestep_mjd
            for i in range(n_steps)
        ])
    else:
        expected_times = np.array([observation.config.start_time_mjd])

    np.testing.assert_allclose(
        observation.times_mjd, expected_times, atol=1e-12, rtol=0.0
    )
    assert np.isclose(
        observation.times_mjd[-1] - observation.times_mjd[0],
        observation.config.observation_length / 86_400.0,
    )


def test_observation_frequencies(observation: Observation):
    """Test that the frequencies property generates correct frequency channels."""

    expected_frequencies = np.array([1e6, 1.5e6])
    np.testing.assert_array_equal(observation.frequencies_hz, expected_frequencies)


def test_observation_single_timestep():
    """Test that the Observation handles single timestep correctly."""
    config = ObservationConfig(
        start_time_mjd=59000.0,
        observation_length=60.0,
        num_timesteps=1,
        start_frequency=1e6,
        num_channels=2,
        total_bandwidth=1e6,
    )
    observation = Observation(config)

    expected_times = np.array([59000.0])
    np.testing.assert_array_equal(observation.times_mjd, expected_times)


def test_observation_phase_centre(observation: Observation):
    """Test that the phase centre is correctly converted to radians."""
    ra_rad, dec_rad = observation.phase_centre_rad
    expected_ra_rad = observation.config.phase_centre_ra * math.pi / 180
    expected_dec_rad = observation.config.phase_centre_dec * math.pi / 180

    assert np.isclose(ra_rad, expected_ra_rad)
    assert np.isclose(dec_rad, expected_dec_rad)


def test_observation_pointing_centre(observation: Observation):
    """Test that the pointing centre is correctly converted to radians."""
    ra_rad, dec_rad = observation.pointing_centre_rad
    expected_ra_rad = observation.config.pointing_centre_ra * math.pi / 180
    expected_dec_rad = observation.config.pointing_centre_dec * math.pi / 180

    assert np.isclose(ra_rad, expected_ra_rad)
    assert np.isclose(dec_rad, expected_dec_rad)


def test_observation_gmst_uses_temporary_iers_settings(
    observation: Observation, monkeypatch
):
    """GMST calculation should temporarily allow stale IERS data offline."""

    original_auto_download = iers.conf.auto_download
    original_auto_max_age = iers.conf.auto_max_age

    def fake_sidereal_time(self, kind, longitude):
        assert kind == "mean"
        assert longitude == "greenwich"
        assert iers.conf.auto_download is False
        assert iers.conf.auto_max_age is None
        return SimpleNamespace(rad=np.array([0.1, 0.2, 0.3]))

    monkeypatch.setattr(Time, "sidereal_time", fake_sidereal_time)

    np.testing.assert_allclose(observation.gmst_rad, np.array([0.1, 0.2, 0.3]))
    assert iers.conf.auto_download is original_auto_download
    assert iers.conf.auto_max_age == original_auto_max_age


def test_uv_coordinates_vary_with_time(observation: Observation):
    """Test that Earth rotation causes U and V coordinates to vary significantly over a long observation."""
    # Single baseline in ECEF coordinates
    baselines_ecef = np.array([[1000.0, 2000.0, 3000.0]])

    # Compute UVW coordinates for all timesteps
    uvw_m = calculate_uvw(
        gmst_rad=observation.gmst_rad,
        phase_centre_rad=observation.phase_centre_rad,
        baselines_ecef_m=baselines_ecef,
    )

    u = uvw_m[:, 0, 0]  # U for the single baseline across all times
    v = uvw_m[:, 0, 1]  # V for the single baseline across all times

    # For a 4-hour observation, U and V should vary significantly
    u_variation = np.max(u) - np.min(u)
    v_variation = np.max(v) - np.min(v)

    # These should be non-zero and substantial (not just numerical noise)
    assert u_variation > 10.0, f"U varied by only {u_variation}, expected > 10"
    assert v_variation > 10.0, f"V varied by only {v_variation}, expected > 10"
