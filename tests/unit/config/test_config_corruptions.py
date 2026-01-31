"""Tests for corruptions configuration."""

import pytest
from starbox.config.corruptions import CorruptionsConfig
from pydantic import ValidationError


def test_corruptions_config_from_dict():
    parameter_dict = {
        "seed": 42,
        "rms_noise": 1.0,
        "rms_phase_gain": 2.0,
    }
    corruptions_config = CorruptionsConfig(**parameter_dict)
    for key, value in parameter_dict.items():
        assert getattr(corruptions_config, key) == value


def test_corruptions_config_rejects_bad_rms_noise():
    with pytest.raises(ValidationError):
        CorruptionsConfig(seed=42, rms_noise=-1.0, rms_phase_gain=2.0)


def test_corruptions_config_valid(corruptions_config):
    assert corruptions_config.seed == 42
    assert corruptions_config.rms_noise == 1.0
    assert corruptions_config.rms_phase_gain == 2.0


def test_corruptions_config_roundtrip_json(corruptions_config):
    """Test that CorruptionsConfig can be serialized to and from JSON."""
    cfg2 = CorruptionsConfig.model_validate_json(corruptions_config.model_dump_json())
    assert cfg2 == corruptions_config


def test_corruptions_config_to_dict(corruptions_config):
    cfg_dict = corruptions_config.model_dump()
    assert cfg_dict["seed"] == corruptions_config.seed
    assert cfg_dict["rms_noise"] == corruptions_config.rms_noise
    assert cfg_dict["rms_phase_gain"] == corruptions_config.rms_phase_gain
