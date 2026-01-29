"""Tests for functions that build observations."""

from starbox.factory.observation import build_observation
from starbox.simulate.observation import Observation


def test_build_observation_returns_observation(observation_config):
    """Test that build_observation returns an Observation instance."""
    observation = build_observation(observation_config)
    assert isinstance(observation, Observation)
    assert observation.start_time == observation_config.start_time
    assert observation.observation_length == observation_config.observation_length
    assert observation.num_timesteps == observation_config.num_timesteps
    assert observation.start_frequency == observation_config.start_frequency
    assert observation.num_channels == observation_config.num_channels
    assert observation.total_bandwidth == observation_config.total_bandwidth
    assert observation.channel_width == (
        observation_config.total_bandwidth / observation_config.num_channels
    )
    assert observation._times is None
    assert observation._frequencies is None
