"""Tests for skymodel classes."""

import pytest
from starbox.simulate.skymodel import SkyModel
from starbox.config.skymodel import SkyModelConfig
import numpy as np


@pytest.mark.parametrize(
    "name,num_sources,max_flux,phase_centre,fov,seed",
    [
        ("TestModel1", 10, 1.0, (0, 0), 1.0, 42),
        ("TestModel2", 100, 5.0, (10, -10), 2.0, 123),
        ("TestModel3", 500, 10.0, (-5, 5), 0.5, 999),
    ],
)
def test_skymodel_config_initialisation(
    name, num_sources, max_flux, phase_centre, fov, seed
):
    """Test that SkyModelConfig initializes with correct parameters."""
    skymodel_config = SkyModelConfig(
        num_sources=num_sources,
        max_flux_jy=max_flux,
        phase_centre_deg=phase_centre,
        fov_deg=fov,
        seed=seed,
    )
    assert skymodel_config.num_sources == num_sources
    assert skymodel_config.max_flux_jy == max_flux
    assert skymodel_config.phase_centre_deg == phase_centre
    assert skymodel_config.fov_deg == fov
    assert skymodel_config.seed == seed


@pytest.mark.parametrize(
    "num_sources,phase_centre,seed",
    [
        (50, (0, 0), 42),
        (200, (20, -20), 123),
    ],
)
def test_skymodel_generate_sources(num_sources, phase_centre, seed):
    """Test that _generate_sources method works correctly."""
    skymodel_config = SkyModelConfig(
        num_sources=num_sources,
        phase_centre_deg=phase_centre,
        fov_deg=1.0,
        max_flux_jy=1.0,
        seed=seed,
    )
    skymodel = SkyModel(skymodel_config)
    config = skymodel.config
    assert skymodel_config == config
    assert len(skymodel.ra_deg) == num_sources
    for ra, dec, flux in zip(skymodel.ra_deg, skymodel.dec_deg, skymodel.flux_jy):
        assert (
            config.phase_centre_deg[0] - config.fov_deg / 2
            <= ra
            <= config.phase_centre_deg[0] + config.fov_deg / 2
        )
        assert (
            config.phase_centre_deg[1] - config.fov_deg / 2
            <= dec
            <= config.phase_centre_deg[1] + config.fov_deg / 2
        )
        assert 0 <= flux <= config.max_flux_jy


def test_skymodel_determinism(skymodel_config):
    """Test that SkyModel generates the same sources with the same seed."""
    skymodel1 = SkyModel(skymodel_config)
    skymodel2 = SkyModel(skymodel_config)
    assert np.array_equal(skymodel1.ra_deg, skymodel2.ra_deg)
    assert np.array_equal(skymodel1.dec_deg, skymodel2.dec_deg)
    assert np.array_equal(skymodel1.flux_jy, skymodel2.flux_jy)


def test_skymodel_variability():
    """Test that different seeds produce different source configurations."""
    skymodel1 = SkyModel(
        SkyModelConfig(
            num_sources=5,
            max_flux_jy=1.0,
            fov_deg=1.0,
            phase_centre_deg=(0.0, 0.0),
            seed=123,
        )
    )
    skymodel2 = SkyModel(
        SkyModelConfig(
            num_sources=5,
            max_flux_jy=1.0,
            fov_deg=1.0,
            phase_centre_deg=(0.0, 0.0),
            seed=456,
        )
    )
    assert not np.array_equal(skymodel1.ra_deg, skymodel2.ra_deg)
    assert not np.array_equal(skymodel1.dec_deg, skymodel2.dec_deg)
    assert not np.array_equal(skymodel1.flux_jy, skymodel2.flux_jy)


def test_skymodel_as_arrays(skymodel):
    """Test that as_arrays method returns correct arrays."""
    ras, decs, fluxes = skymodel.as_arrays()
    config = skymodel.config
    assert config is not None
    assert len(ras) == config.num_sources
    assert len(decs) == config.num_sources
    assert len(fluxes) == config.num_sources
    np.testing.assert_array_equal(ras, skymodel.ra_deg)
    np.testing.assert_array_equal(decs, skymodel.dec_deg)
    np.testing.assert_array_equal(fluxes, skymodel.flux_jy)


def test_skymodel_equality(skymodel_config):
    """Test the equality check between two SkyModel instances."""
    skymodel1 = SkyModel(skymodel_config)
    skymodel2 = SkyModel(skymodel_config)
    assert skymodel1.equals(skymodel2, atol=1e-8, rtol=1e-5)

    # Modify skymodel2 slightly
    skymodel2.ra_deg[0] += 1e-6
    assert not skymodel1.equals(skymodel2, atol=1e-8, rtol=1e-8)
    assert skymodel1.equals(skymodel2, atol=1e-5, rtol=1e-3)
