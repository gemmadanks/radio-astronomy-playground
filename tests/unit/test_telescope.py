"""Test the Telescope class."""

from starbox.simulate.telescope import Telescope, _compute_coordinates
from starbox.config import TelescopeConfig, TelescopeSiteConfig
import numpy as np


def test_telescope_site_initialisation():
    """Test that a TelescopeSiteConfig object initialises correctly."""
    site_config = TelescopeSiteConfig(latitude_deg=45.0, longitude_deg=90.0, altitude_m=100.0)
    assert site_config.latitude_deg == 45.0
    assert site_config.longitude_deg == 90.0
    assert site_config.altitude_m == 100.0


def test_telescope_initialisation(telescope_site_config):
    """Test that a Telescope object initialises correctly from a TelescopeConfig."""
    config = TelescopeConfig(num_stations=100, diameter=50.0, seed=42, site=telescope_site_config)
    telescope = Telescope(config, name="ELA")
    assert telescope.name == "ELA"
    assert telescope.config.num_stations == 100
    assert telescope.config.diameter == 50.0
    assert telescope.station_positions is not None
    assert telescope.station_positions.shape == (100, 3)
    np.testing.assert_array_equal(
        telescope.station_ids, np.array([f"ELA_STN{idx:03d}" for idx in range(100)])
    )


def test_telescope_array_determinism(telescope_site_config):
    """Test that the array configuration is deterministic given the same seed."""
    config1 = TelescopeConfig(num_stations=50, diameter=30.0, seed=123, site=telescope_site_config)
    telescope1 = Telescope(config1, name="DeterministicArray")
    config2 = TelescopeConfig(num_stations=50, diameter=30.0, seed=123, site=telescope_site_config)
    telescope2 = Telescope(config2, name="DeterministicArray")
    assert telescope1.station_positions is not None
    assert telescope2.station_positions is not None
    np.testing.assert_array_equal(
        telescope1.station_positions, telescope2.station_positions
    )


def test_telescope_array_variability(telescope_site_config):
    """Test that different seeds produce different array configurations."""
    config1 = TelescopeConfig(num_stations=50, diameter=30.0, seed=123, site=telescope_site_config)
    telescope1 = Telescope(config1, name="VariableArray")
    config2 = TelescopeConfig(num_stations=50, diameter=30.0, seed=456, site=telescope_site_config)
    telescope2 = Telescope(config2, name="VariableArray")

    assert telescope1.station_positions is not None
    assert telescope2.station_positions is not None
    assert not np.array_equal(
        telescope1.station_positions, telescope2.station_positions
    )


def test_telescope_get_angles(small_telescope):
    """Test that _get_angles returns an array of the correct length and values within the expected range."""
    angles = small_telescope._get_angles()
    assert len(angles) == 10
    assert (angles >= 0).all() and (angles <= 2 * np.pi).all()


def test_telescope_get_radii(small_telescope):
    """Test that _get_radii returns an array of the correct length and values within the expected range."""
    radii = small_telescope._get_radii()
    assert len(radii) == 10
    assert (radii >= 0).all() and (radii <= small_telescope.config.diameter / 2).all()


def test_telescope_compute_coordinates():
    """Test that _compute_coordinates returns arrays of the correct length."""
    angles = np.array([0.1] * 10)
    radii = np.array([5.0] * 10)
    x, y, z = _compute_coordinates(angles, radii)
    assert len(x) == 10
    assert len(y) == 10
    assert len(z) == 10
