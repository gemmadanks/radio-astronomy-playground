"""Tests for Observation class."""

from starbox.config.observation import ObservationConfig
from starbox.simulate import Observation
import numpy as np


def test_observation_from_config(observation_config):
    """Test that Observation can be created from ObservationConfig."""

    observation = Observation(observation_config)

    assert observation.config == observation_config
    assert observation.channel_width == (
        observation_config.total_bandwidth / observation_config.num_channels
    )
    assert observation.times is not None
    assert observation.frequencies is not None


def test_observation_times(observation: Observation):
    """Test that the times property generates correct time steps."""

    expected_times = np.array([0.0, 90.0, 180.0])
    np.testing.assert_array_equal(observation.times, expected_times)
    assert (
        observation.times[-1] - observation.times[0]
        == observation.config.observation_length
    )


def test_observation_frequencies(observation: Observation):
    """Test that the frequencies property generates correct frequency channels."""

    expected_frequencies = np.array([1e6, 1.5e6])
    np.testing.assert_array_equal(observation.frequencies, expected_frequencies)


def test_observation_single_timestep():
    """Test that the Observation handles single timestep correctly."""
    config = ObservationConfig(
        start_time=0,
        observation_length=60.0,
        num_timesteps=1,
        start_frequency=1e6,
        num_channels=2,
        total_bandwidth=1e6,
    )
    observation = Observation(config)

    expected_times = np.array([0])
    np.testing.assert_array_equal(observation.times, expected_times)
