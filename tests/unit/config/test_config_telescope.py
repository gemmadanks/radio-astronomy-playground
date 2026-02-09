"""Tests for Telescope configuration."""

import pytest
from starbox.config.telescope import TelescopeConfig
from pydantic import ValidationError


def test_telescope_config_from_dict(telescope_site_config):
    parameter_dict = {
        "num_stations": 50,
        "diameter": 30.0,
        "seed": 123,
        "site": telescope_site_config,
    }
    telescope_config = TelescopeConfig(**parameter_dict)
    for key, value in parameter_dict.items():
        assert getattr(telescope_config, key) == value


def test_telescope_config_valid(telescope_site_config):
    cfg = TelescopeConfig(
        num_stations=10, diameter=25.0, seed=0, site=telescope_site_config
    )
    assert cfg.num_stations == 10
    assert cfg.diameter == 25.0
    assert cfg.seed == 0


def test_telescope_config_rejects_bad_num_stations(telescope_site_config):
    with pytest.raises(ValidationError):
        TelescopeConfig(
            num_stations=0, diameter=25.0, seed=0, site=telescope_site_config
        )


def test_telescope_config_rejects_bad_diameter(telescope_site_config):
    with pytest.raises(ValidationError):
        TelescopeConfig(
            num_stations=10, diameter=-5.0, seed=0, site=telescope_site_config
        )


def test_telescope_config_roundtrip_json(telescope_site_config):
    cfg = TelescopeConfig(
        num_stations=10, diameter=25.0, seed=0, site=telescope_site_config
    )
    cfg2 = TelescopeConfig.model_validate_json(cfg.model_dump_json())
    assert cfg2 == cfg


def test_telescope_config_to_dict(telescope_site_config):
    cfg = TelescopeConfig(
        num_stations=10, diameter=25.0, seed=0, site=telescope_site_config
    )
    cfg_dict = cfg.model_dump()
    assert cfg_dict["num_stations"] == 10
    assert cfg_dict["diameter"] == 25.0
    assert cfg_dict["seed"] == 0
    assert cfg_dict["site"] == telescope_site_config.model_dump()
