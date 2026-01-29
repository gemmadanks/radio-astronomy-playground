"""Tests for Observation class."""

from starbox.simulate import Observation, ObservationSpec
import numpy as np
import pytest


def test_observation_spec_initialization(observation_spec):
    """Test that the ObservationSpec initializes correctly."""

    assert observation_spec.start_time == 0
    assert observation_spec.observation_length == 180.0
    assert observation_spec.num_timesteps == 3
    assert observation_spec.start_frequency == 1e6
    assert observation_spec.num_channels == 2
    assert observation_spec.total_bandwidth == 1e6


def test_observation_spec_invalid_num_channels():
    """Test that the ObservationSpec raises an error for invalid num_channels."""

    with pytest.raises(ValueError, match="num_channels must be a positive integer"):
        ObservationSpec(
            start_time=0,
            observation_length=60.0,
            num_timesteps=2,
            start_frequency=1e6,
            num_channels=0,
            total_bandwidth=1e6,
        )


def test_observation_spec_invalid_num_timesteps():
    """Test that the ObservationSpec raises an error for invalid num_timesteps."""

    with pytest.raises(ValueError, match="num_timesteps must be a positive integer"):
        ObservationSpec(
            start_time=0,
            observation_length=60.0,
            num_timesteps=-1,
            start_frequency=1e6,
            num_channels=2,
            total_bandwidth=1e6,
        )


def test_observation_from_spec(observation_spec):
    """Test that Observation can be created from ObservationSpec."""

    observation = Observation.from_spec(observation_spec)

    assert observation.start_time == observation_spec.start_time
    assert observation.observation_length == observation_spec.observation_length
    assert observation.num_timesteps == observation_spec.num_timesteps
    assert observation.start_frequency == observation_spec.start_frequency
    assert observation.num_channels == observation_spec.num_channels
    assert observation.total_bandwidth == observation_spec.total_bandwidth
    assert observation.spec == observation_spec
    assert observation.channel_width == (
        observation_spec.total_bandwidth / observation_spec.num_channels
    )
    assert observation._times is None
    assert observation._frequencies is None


def test_observation_times(observation: Observation):
    """Test that the times property generates correct time steps."""

    expected_times = np.array([0.0, 90.0, 180.0])
    np.testing.assert_array_equal(observation.times, expected_times)
    assert (
        observation.times[-1] - observation.times[0] == observation.observation_length
    )


def test_observation_frequencies(observation: Observation):
    """Test that the frequencies property generates correct frequency channels."""

    expected_frequencies = np.array([1e6, 1.5e6])
    np.testing.assert_array_equal(observation.frequencies, expected_frequencies)


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
    np.testing.assert_array_equal(observation.times, expected_times)
