"""Tests for skymodel classes."""

import pytest
from starbox.simulate.skymodel import SkyModel, SkyModelSpec
import numpy as np


@pytest.mark.parametrize(
    "name,num_sources,max_flux,phase_centre,fov,seed",
    [
        ("TestModel1", 10, 1.0, (0, 0), 1.0, 42),
        ("TestModel2", 100, 5.0, (10, -10), 2.0, 123),
        ("TestModel3", 500, 10.0, (-5, 5), 0.5, 999),
    ],
)
def test_skymodel_spec_intialisation(
    name, num_sources, max_flux, phase_centre, fov, seed
):
    """Test that SkyModelSpec initializes with correct parameters."""
    skymodel_spec = SkyModelSpec(
        num_sources=num_sources,
        max_flux_jy=max_flux,
        phase_centre_deg=phase_centre,
        fov_deg=fov,
        seed=seed,
    )
    assert skymodel_spec.num_sources == num_sources
    assert skymodel_spec.max_flux_jy == max_flux
    assert skymodel_spec.phase_centre_deg == phase_centre
    assert skymodel_spec.fov_deg == fov
    assert skymodel_spec.seed == seed


@pytest.mark.parametrize(
    "name,num_sources,phase_centre,seed",
    [
        ("TestModel", 50, (0, 0), 42),
        ("TestModel", 200, (20, -20), 123),
    ],
)
def test_skymodel_generate_sources(name, num_sources, phase_centre, seed):
    """Test that _generate_sources method works correctly."""
    skymodel_spec = SkyModelSpec(
        num_sources=num_sources, phase_centre_deg=phase_centre, seed=seed
    )
    skymodel = SkyModel.from_spec(skymodel_spec)
    spec = skymodel.spec
    assert spec is not None
    assert len(skymodel.ra_deg) == num_sources
    for ra, dec, flux in zip(skymodel.ra_deg, skymodel.dec_deg, skymodel.flux_jy):
        assert (
            spec.phase_centre_deg[0] - spec.fov_deg / 2
            <= ra
            <= spec.phase_centre_deg[0] + spec.fov_deg / 2
        )
        assert (
            spec.phase_centre_deg[1] - spec.fov_deg / 2
            <= dec
            <= spec.phase_centre_deg[1] + spec.fov_deg / 2
        )
        assert 0 <= flux <= spec.max_flux_jy


def test_skymodel_determinism(skymodel_spec):
    """Test that SkyModel generates the same sources with the same seed."""
    skymodel1 = SkyModel.from_spec(skymodel_spec)
    skymodel2 = SkyModel.from_spec(skymodel_spec)
    assert np.array_equal(skymodel1.ra_deg, skymodel2.ra_deg)
    assert np.array_equal(skymodel1.dec_deg, skymodel2.dec_deg)
    assert np.array_equal(skymodel1.flux_jy, skymodel2.flux_jy)


def test_skymodel_variability():
    """Test that different seeds produce different source configurations."""
    skymodel1 = SkyModel.from_spec(SkyModelSpec(num_sources=20, seed=123))
    skymodel2 = SkyModel.from_spec(SkyModelSpec(num_sources=20, seed=456))
    assert not np.array_equal(skymodel1.ra_deg, skymodel2.ra_deg)
    assert not np.array_equal(skymodel1.dec_deg, skymodel2.dec_deg)
    assert not np.array_equal(skymodel1.flux_jy, skymodel2.flux_jy)


def test_skymodel_as_arrays(skymodel):
    """Test that as_arrays method returns correct arrays."""
    ras, decs, fluxes = skymodel.as_arrays()
    spec = skymodel.spec
    assert spec is not None
    assert len(ras) == spec.num_sources
    assert len(decs) == spec.num_sources
    assert len(fluxes) == spec.num_sources
    np.testing.assert_array_equal(ras, skymodel.ra_deg)
    np.testing.assert_array_equal(decs, skymodel.dec_deg)
    np.testing.assert_array_equal(fluxes, skymodel.flux_jy)


@pytest.mark.parametrize("num_sources", [0, -5, -10])
def test_skymodel_spec_invalid_num_sources_raises_error(num_sources):
    """Test that SkyModelSpec with no sources behaves correctly."""
    with pytest.raises(ValueError, match="num_sources must be > 0"):
        SkyModelSpec(num_sources=num_sources)


@pytest.mark.parametrize("max_flux", [0.0, -0.1, -10.0])
def test_skymodel_spec_invalid_flux_raises_error(max_flux):
    """Test that SkyModelSpec with zero or negative max_flux raises error."""
    with pytest.raises(ValueError, match="max_flux_jy must be > 0"):
        SkyModelSpec(num_sources=10, max_flux_jy=max_flux)


@pytest.mark.parametrize("fov", [0, -1.0])
def test_skymodel_spec_invalid_fov_raises_error(fov):
    """Test that SkyModelSpec with non-positive fov raises error."""
    with pytest.raises(ValueError, match="fov_deg must be > 0"):
        SkyModelSpec(num_sources=10, fov_deg=fov)


def test_skymodel_spec_repr(skymodel_spec):
    """Test the __repr__ method of SkyModelSpec."""
    repr_str = repr(skymodel_spec)
    expected_str = (
        "SkyModelSpec(num_sources=5, max_flux_jy=1.0, "
        "phase_centre_deg=(0, 0), fov_deg=1.0, seed=42)"
    )
    assert repr_str == expected_str
