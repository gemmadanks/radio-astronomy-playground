"""Tests for Observation class."""

from starbox.simulate import Observation
import numpy as np


def test_observation_initialization():
    """Test that the Observation initializes correctly."""

    observation = Observation(
        start_time=0,
        observation_length=120.0,
        num_timesteps=3,
        start_frequency=1e6,
        num_channels=2,
        total_bandwidth=1e6,
    )

    assert observation.start_time == 0
    assert observation.observation_length == 120.0
    assert observation.num_timesteps == 3
    assert observation.start_frequency == 1e6
    assert observation.num_channels == 2
    assert observation.total_bandwidth == 1e6
    assert observation.channel_width == 500000.0


def test_observation_times(observation: Observation):
    """Test that the times property generates correct time steps."""

    expected_times = np.array([0.0, 90.0, 180.0])
    assert (observation.times == expected_times).all()
    assert (
        observation.times[-1] - observation.times[0] == observation.observation_length
    )


def test_observation_frequencies(observation: Observation):
    """Test that the frequencies property generates correct frequency channels."""

    expected_frequencies = np.array([1e6, 1.5e6])
    assert (observation.frequencies == expected_frequencies).all()


def test_observation_single_timestep():
    """Test that the Observation handles single timestep correctly."""

    observation = Observation(
        start_time=0,
        observation_length=60.0,
        num_timesteps=1,
        start_frequency=1e6,
        num_channels=2,
        total_bandwidth=1e6,
    )

    expected_times = np.array([0])
    assert (observation.times == expected_times).all()
