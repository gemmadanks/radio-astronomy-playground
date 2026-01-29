"""Tests for functions that build sky models."""

from starbox.factory.skymodel import build_skymodel
from starbox.simulate.skymodel import SkyModel


def test_build_skymodel_returns_skymodel(skymodel_config):
    """Test that build_skymodel returns a SkyModel instance."""
    skymodel = build_skymodel(skymodel_config)
    assert isinstance(skymodel, SkyModel)
    assert len(skymodel.ra_deg) == skymodel_config.num_sources
    assert len(skymodel.dec_deg) == skymodel_config.num_sources
    assert len(skymodel.flux_jy) == skymodel_config.num_sources
