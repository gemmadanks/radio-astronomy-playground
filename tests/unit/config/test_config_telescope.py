"""Tests for Telescope configuration."""

import pytest
from starbox.config.telescope import TelescopeConfig
from pydantic import ValidationError


def test_telescope_config_from_dict():
    parameter_dict = {
        "num_stations": 50,
        "diameter": 30.0,
        "seed": 123,
    }
    telescope_config = TelescopeConfig(**parameter_dict)
    for key, value in parameter_dict.items():
        assert getattr(telescope_config, key) == value


def test_telescope_config_valid():
    cfg = TelescopeConfig(num_stations=10, diameter=25.0, seed=0)
    assert cfg.num_stations == 10
    assert cfg.diameter == 25.0
    assert cfg.seed == 0


def test_telescope_config_rejects_bad_num_stations():
    with pytest.raises(ValidationError):
        TelescopeConfig(num_stations=0, diameter=25.0, seed=0)


def test_telescope_config_rejects_bad_diameter():
    with pytest.raises(ValidationError):
        TelescopeConfig(num_stations=10, diameter=-5.0, seed=0)


def test_telescope_config_roundtrip_json():
    cfg = TelescopeConfig(num_stations=10, diameter=25.0, seed=0)
    cfg2 = TelescopeConfig.model_validate_json(cfg.model_dump_json())
    assert cfg2 == cfg


def test_telescope_config_to_dict():
    cfg = TelescopeConfig(num_stations=10, diameter=25.0, seed=0)
    cfg_dict = cfg.model_dump()
    assert cfg_dict["num_stations"] == 10
    assert cfg_dict["diameter"] == 25.0
    assert cfg_dict["seed"] == 0
