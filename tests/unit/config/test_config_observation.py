"""Tests for Observation configuration."""

from starbox.config.observation import ObservationConfig


def test_observation_config_from_dict():
    parameter_dict = {
        "start_time": 59000.0,
        "observation_length": 3600,
        "num_timesteps": 10,
        "start_frequency": 100.0,
        "total_bandwidth": 10.0,
        "num_channels": 5,
    }
    observation_config = ObservationConfig(**parameter_dict)
    for key, value in parameter_dict.items():
        assert getattr(observation_config, key) == value


def test_observation_config_roundtrip_json(observation_config):
    """Test that ObservationConfig can be serialized to and from JSON."""
    cfg2 = ObservationConfig.model_validate_json(observation_config.model_dump_json())
    assert cfg2 == observation_config
