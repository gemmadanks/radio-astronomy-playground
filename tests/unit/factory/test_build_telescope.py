"""Tests for functions that build telescopes."""

from starbox.factory.telescope import build_telescope
from starbox.simulate.telescope import Telescope


def test_build_telescope_returns_telescope(telescope_config):
    """Test that build_telescope returns a Telescope instance."""
    telescope = build_telescope(telescope_config)

    assert isinstance(telescope, Telescope)
    assert telescope.config == telescope_config
    assert telescope.array.shape == (telescope_config.num_stations, 3)
    assert len(telescope.station_ids) == telescope_config.num_stations
