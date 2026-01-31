"""Tests for functions that build observations."""

from starbox.factory.observation import build_observation
from starbox.simulate.observation import Observation


def test_build_observation_returns_observation(observation_config):
    """Test that build_observation returns an Observation instance."""
    observation = build_observation(observation_config)
    assert isinstance(observation, Observation)
    assert observation.config == observation_config
    assert observation.channel_width == (
        observation_config.total_bandwidth / observation_config.num_channels
    )
    assert observation.times.shape == (observation_config.num_timesteps,)
    assert observation.frequencies.shape == (observation_config.num_channels,)
