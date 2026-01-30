"""Tests for functions that build telescopes."""

from starbox.factory.telescope import build_telescope
from starbox.simulate.telescope import Telescope


def test_build_telescope_returns_telescope(telescope_config):
    """Test that build_telescope returns a Telescope instance."""
    telescope = build_telescope(telescope_config)

    assert isinstance(telescope, Telescope)
    assert telescope.num_stations == telescope_config.num_stations
    assert telescope.diameter == telescope_config.diameter
    assert telescope.seed == telescope_config.seed
    assert telescope.array is not None
    assert telescope.array.shape == (telescope_config.num_stations, 3)
    assert telescope.station_ids is not None
    assert len(telescope.station_ids) == telescope_config.num_stations
