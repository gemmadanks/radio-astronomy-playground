"""Tests for Observation class."""

from types import SimpleNamespace

from astropy.time import Time
from astropy.utils import iers
from starbox.config.observation import ObservationConfig
from starbox.simulate import Observation
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

    expected_times = np.array(
        [
            observation.config.start_time_mjd,
            observation.config.start_time_mjd + 90.0 / 86_400.0,
            observation.config.start_time_mjd + 180.0 / 86_400.0,
        ]
    )
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
