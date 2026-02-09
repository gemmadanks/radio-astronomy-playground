"""Test the Telescope class."""

from starbox.simulate.telescope import Telescope, _compute_enu_coordinates
from starbox.config import TelescopeConfig, TelescopeSiteConfig
import numpy as np


def test_telescope_site_initialisation():
    """Test that a TelescopeSiteConfig object initialises correctly."""
    site_config = TelescopeSiteConfig(
        latitude_deg=45.0, longitude_deg=90.0, altitude_m=100.0
    )
    assert site_config.latitude_deg == 45.0
    assert site_config.longitude_deg == 90.0
    assert site_config.altitude_m == 100.0


def test_telescope_initialisation(telescope_site_config):
    """Test that a Telescope object initialises correctly from a TelescopeConfig."""
    config = TelescopeConfig(
        num_stations=100, diameter=50.0, seed=42, site=telescope_site_config
    )
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
    config1 = TelescopeConfig(
        num_stations=50, diameter=30.0, seed=123, site=telescope_site_config
    )
    telescope1 = Telescope(config1, name="DeterministicArray")
    config2 = TelescopeConfig(
        num_stations=50, diameter=30.0, seed=123, site=telescope_site_config
    )
    telescope2 = Telescope(config2, name="DeterministicArray")
    assert telescope1.station_positions is not None
    assert telescope2.station_positions is not None
    np.testing.assert_array_equal(
        telescope1.station_positions, telescope2.station_positions
    )


def test_telescope_array_variability(telescope_site_config):
    """Test that different seeds produce different array configurations."""
    config1 = TelescopeConfig(
        num_stations=50, diameter=30.0, seed=123, site=telescope_site_config
    )
    telescope1 = Telescope(config1, name="VariableArray")
    config2 = TelescopeConfig(
        num_stations=50, diameter=30.0, seed=456, site=telescope_site_config
    )
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
    east, north, up = _compute_enu_coordinates(angles, radii)
    assert len(east) == 10
    assert len(north) == 10
    assert len(up) == 10


def test_telescope_enu_to_ecef_shape(small_telescope):
    """Test that _enu_to_ecef returns an array of the correct shape."""
    ecef_coords = small_telescope._enu_to_ecef()
    assert ecef_coords.shape == (small_telescope.config.num_stations, 3)


def test_telescope_enu_to_ecef_origin():
    """Test that _enu_to_ecef returns the correct ECEF coordinates for a telescope with zero ENU coordinates."""
    site_config = TelescopeSiteConfig(
        latitude_deg=0.0, longitude_deg=0.0, altitude_m=0.0
    )
    config = TelescopeConfig(num_stations=1, diameter=1.0, seed=42, site=site_config)
    telescope = Telescope(config, name="ZeroENU")
    telescope.station_positions = np.array(
        [[0.0, 0.0, 0.0]]
    )  # Override station positions to be at the origin
    ecef_coords = telescope._enu_to_ecef()
    expected_ecef = np.array([[0.0, 0.0, 0.0]])
    np.testing.assert_array_almost_equal(ecef_coords, expected_ecef)


def test_telescope_enu_to_ecef_equator_and_prime_meridian():
    """Test that _enu_to_ecef returns the correct ECEF coordinates for a telescope located at the equator and prime meridian."""
    site_config = TelescopeSiteConfig(
        latitude_deg=0.0, longitude_deg=0.0, altitude_m=0.0
    )
    config = TelescopeConfig(num_stations=3, diameter=1.0, seed=42, site=site_config)
    telescope = Telescope(config, name="EquatorPrimeMeridian")
    telescope.station_positions = np.array(
        [  # Override station positions
            [1.0, 0.0, 0.0],  # 1 meter east
            [0.0, 1.0, 0.0],  # 1 meter north
            [0.0, 0.0, 1.0],  # 1 meter up
        ]
    )
    expected_ecef = np.array(
        [
            [0.0, 1.0, 0.0],  # 1 meter east in ECEF
            [0.0, 0.0, 1.0],  # 1 meter north in ECEF
            [1.0, 0.0, 0.0],  # 1 meter up in ECEF
        ]
    )
    actual_ecef = telescope._enu_to_ecef()
    np.testing.assert_array_almost_equal(actual_ecef, expected_ecef)


def test_rotation_matrix_is_orthonormal(small_telescope):
    """Test that the rotation matrix used in _enu_to_ecef is orthonormal."""
    rotation_matrix = small_telescope._rotation_matrix()
    identity = np.eye(3)
    np.testing.assert_array_almost_equal(rotation_matrix @ rotation_matrix.T, identity)


def test_telescope_compute_baselines(small_telescope):
    """Test that _compute_baselines returns the correct number of baselines."""
    baselines = small_telescope._compute_baselines(small_telescope._enu_to_ecef())
    num_stations = small_telescope.config.num_stations
    expected_num_baselines = num_stations * (num_stations - 1) // 2
    assert baselines.shape == (expected_num_baselines, 3)


def test_telescope_enu_to_ecef_consistency(small_telescope):
    """Test that the ENU to ECEF conversion is consistent with the original ENU coordinates."""
    enu_coords = small_telescope.station_positions
    ecef_coords = small_telescope._enu_to_ecef()
    # Convert back from ECEF to ENU using the inverse rotation
    rotation_matrix = small_telescope._rotation_matrix()
    enu_from_ecef = ecef_coords @ rotation_matrix
    np.testing.assert_array_almost_equal(enu_coords, enu_from_ecef)


def test_telescope_baselines_commute_with_rotation(small_telescope):
    rotation_matrix = small_telescope._rotation_matrix()
    baselines_enu = small_telescope._compute_baselines(
        small_telescope.station_positions
    )
    baselines_enu_rotated = baselines_enu @ rotation_matrix.T
    baselines_ecef = small_telescope._compute_baselines(small_telescope._enu_to_ecef())

    np.testing.assert_allclose(
        baselines_ecef, baselines_enu_rotated, rtol=0, atol=1e-10
    )
