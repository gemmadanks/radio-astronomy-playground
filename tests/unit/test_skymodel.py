"""Tests for skymodel classes."""

import pytest
from starbox.simulate.skymodel import SkyModel


@pytest.mark.parametrize(
    "name,num_sources,max_flux,phase_centre,fov,seed",
    [
        ("TestModel1", 10, 1.0, (0, 0), 1.0, 42),
        ("TestModel2", 100, 5.0, (10, -10), 2.0, 123),
        ("TestModel3", 500, 10.0, (-5, 5), 0.5, 999),
    ],
)
def test_skymodel_parameters(name, num_sources, max_flux, phase_centre, fov, seed):
    """Test that SkyModel initializes with correct parameters."""
    skymodel = SkyModel(
        name=name,
        num_sources=num_sources,
        max_flux=max_flux,
        phase_centre=phase_centre,
        fov=fov,
        seed=seed,
    )
    assert skymodel.name == name
    assert skymodel.num_sources == num_sources
    assert skymodel.max_flux == max_flux
    assert skymodel.phase_centre == phase_centre
    assert skymodel.fov == fov
    assert skymodel.rng is not None
    assert len(skymodel.sources) == num_sources


@pytest.mark.parametrize(
    "name,num_sources,phase_centre,seed",
    [
        ("TestModel", 50, (0, 0), 42),
        ("TestModel", 200, (20, -20), 123),
    ],
)
def test_skymodel_generate_sources(name, num_sources, phase_centre, seed):
    """Test that _generate_sources method works correctly."""
    skymodel = SkyModel(
        name="TestModel", num_sources=num_sources, phase_centre=phase_centre, seed=seed
    )
    assert len(skymodel.sources) == num_sources
    for pos, flux in skymodel.sources:
        ra, dec = pos
        assert (
            skymodel.phase_centre[0] - skymodel.fov / 2
            <= ra
            <= skymodel.phase_centre[0] + skymodel.fov / 2
        )
        assert (
            skymodel.phase_centre[1] - skymodel.fov / 2
            <= dec
            <= skymodel.phase_centre[1] + skymodel.fov / 2
        )
        assert 0 <= flux <= skymodel.max_flux


def test_skymodel_determinism():
    """Test that SkyModel generates the same sources with the same seed."""
    skymodel1 = SkyModel(name="TestModel1", num_sources=20, seed=123)
    skymodel2 = SkyModel(name="TestModel2", num_sources=20, seed=123)
    assert skymodel1.sources == skymodel2.sources


def test_skymodel_variability():
    """Test that different seeds produce different source configurations."""
    skymodel1 = SkyModel(name="TestModel1", num_sources=20, seed=123)
    skymodel2 = SkyModel(name="TestModel2", num_sources=20, seed=456)
    assert skymodel1.sources != skymodel2.sources


def test_skymodel_regenerate():
    """Test that regenerate changes the source configuration."""
    skymodel = SkyModel(name="TestModel", num_sources=30, seed=42)
    original_sources = skymodel.sources.copy()
    skymodel.regenerate(seed=43)
    new_sources = skymodel.sources
    assert original_sources != new_sources
