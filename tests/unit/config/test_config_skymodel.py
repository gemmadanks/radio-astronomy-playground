"""Tests for SkyModel configuration."""

from starbox.config.skymodel import SkyModelConfig
import pytest
from pydantic import ValidationError
from starbox.simulate.skymodel import SkyModelSpec


def test_skymodel_config_from_dict():
    parameter_dict = {
        "num_sources": 100,
        "max_flux_jy": 5.0,
        "phase_centre_deg": (10, -10),
        "fov_deg": 2.0,
        "seed": 42,
    }
    skymodel_config = SkyModelConfig(**parameter_dict)
    for key, value in parameter_dict.items():
        assert getattr(skymodel_config, key) == value


def test_skymodel_config_valid():
    cfg = SkyModelConfig(num_sources=5, max_flux_jy=1.0, fov_deg=1.0, seed=0)
    assert cfg.num_sources == 5


def test_skymodel_config_rejects_bad_num_sources():
    with pytest.raises(ValidationError):
        SkyModelConfig(num_sources=0, max_flux_jy=1.0, fov_deg=1.0, seed=0)


@pytest.mark.parametrize("bad_fov", [-1.0, 0.0])
def test_skymodel_config_rejects_bad_fov(bad_fov):
    with pytest.raises(ValidationError):
        SkyModelConfig(num_sources=5, max_flux_jy=1.0, fov_deg=bad_fov, seed=0)


@pytest.mark.parametrize("bad_max_flux_jy", [-1.0, 0.0])
def test_skymodel_config_rejects_bad_max_flux_jy(bad_max_flux_jy):
    with pytest.raises(ValidationError):
        SkyModelConfig(num_sources=5, max_flux_jy=bad_max_flux_jy, fov_deg=1.0, seed=0)


def test_skymodel_config_roundtrip_json():
    cfg = SkyModelConfig(num_sources=5, max_flux_jy=1.0, fov_deg=1.0, seed=0)
    cfg2 = SkyModelConfig.model_validate_json(cfg.model_dump_json())
    assert cfg2 == cfg


def test_skymodel_config_to_spec():
    cfg = SkyModelConfig(num_sources=5, max_flux_jy=1.0, fov_deg=1.0, seed=0)
    spec = SkyModelSpec(**cfg.model_dump())
    assert spec.num_sources == cfg.num_sources
    assert spec.max_flux_jy == cfg.max_flux_jy
    assert spec.phase_centre_deg == cfg.phase_centre_deg
    assert spec.fov_deg == cfg.fov_deg
    assert spec.seed == cfg.seed
