"""Tests for Observation class."""

from starbox.simulate import Observation


def test_observation_init(observation: Observation):
    """Test that the Observation class initializes correctly."""

    expected_times = [0, 60.0, 120.0]
    expected_frequencies = [1e6, 1.5e6]

    observation.times == expected_times
    observation.frequencies == expected_frequencies
