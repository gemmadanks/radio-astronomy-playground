"""Test the Telescope class."""

import pytest
import re

from starbox.simulate.telescope import Telescope, _compute_coordinates, TelescopeSpec
import numpy as np


def test_telescope_spec_initialization():
    """Test that TelescopeSpec initializes with correct parameters."""
    spec = TelescopeSpec(num_stations=50, diameter=30.0, seed=42)
    assert spec.num_stations == 50
    assert spec.diameter == 30.0
    assert spec.seed == 42


def test_telescope_spec_invalid_num_stations():
    """Test that TelescopeSpec raises error for invalid num_stations."""
    with pytest.raises(ValueError, match="num_stations must be > 0"):
        TelescopeSpec(num_stations=0, diameter=30.0)
    with pytest.raises(ValueError, match="num_stations must be > 0"):
        TelescopeSpec(num_stations=-10, diameter=30.0)


def test_telescope_spec_invalid_diameter():
    """Test that TelescopeSpec raises error for invalid diameter."""
    with pytest.raises(ValueError, match="diameter must be > 0"):
        TelescopeSpec(num_stations=10, diameter=0.0)
    with pytest.raises(ValueError, match="diameter must be > 0"):
        TelescopeSpec(num_stations=10, diameter=-5.0)


def test_telescope_from_spec():
    """Test that a Telescope object initializes correctly from a TelescopeSpec."""
    spec = TelescopeSpec(num_stations=100, diameter=50.0)
    telescope = Telescope.from_spec(spec, name="ELA")
    assert telescope.name == "ELA"
    assert telescope.num_stations == 100
    assert telescope.diameter == 50.0
    assert telescope.array is not None
    assert telescope.array.shape == (100, 3)
    np.testing.assert_array_equal(
        telescope.station_ids, np.array([f"ELA_STN{idx:03d}" for idx in range(100)])
    )


@pytest.mark.parametrize(
    "name,num_stations,diameter,seed",
    [
        ("SmallArray", 10, 5.0, 10),
        ("SmallArrayDifferentSeed", 10, 5.0, 11),
        ("LargeArray", 2000, 250.0, 42),
    ],
)
def test_telescope_array(name, num_stations, diameter, seed):
    """Test that array returns a numpy array of antenna positions."""
    spec = TelescopeSpec(num_stations=num_stations, diameter=diameter, seed=seed)
    telescope = Telescope.from_spec(spec, name=name)
    array = telescope.array
    assert array is not None
    assert array.shape == (num_stations, 3)
    assert array.dtype == float
    assert array.max() <= diameter
    np.testing.assert_array_equal(
        telescope.station_ids,
        np.array([f"{name}_STN{idx:03d}" for idx in range(num_stations)]),
    )


def test_telescope_array_supplied(mocker):
    """Test that supplying an array works correctly."""
    num_stations = 5
    diameter = 10.0
    array = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.5, 0.5, 0.0],
        ]
    )
    spy_ = mocker.spy(Telescope, "_configure_array")
    telescope = Telescope(
        name="CustomArray", num_stations=num_stations, array=array, diameter=diameter
    )
    assert spy_.call_count == 0  # _configure_array should not be called
    assert telescope.array is not None
    assert telescope.array.shape == (num_stations, 3)
    np.testing.assert_array_equal(telescope.array, array)
    np.testing.assert_array_equal(
        telescope.station_ids,
        np.array([f"CustomArray_STN{idx:03d}" for idx in range(num_stations)]),
    )


def test_telescope_station_ids_supplied(mocker):
    """Test that supplying station IDs works correctly."""
    num_stations = 3
    diameter = 10.0
    station_ids = np.array(["STA001", "STA002", "STA003"])
    spy_ = mocker.spy(Telescope, "_configure_array")
    telescope = Telescope(
        name="CustomIDs",
        num_stations=num_stations,
        station_ids=station_ids,
        diameter=diameter,
    )
    assert spy_.call_count == 1  # _configure_array should be called
    assert telescope.station_ids is not None
    assert telescope.array is not None
    assert telescope.station_ids.shape == (num_stations,)
    np.testing.assert_array_equal(telescope.station_ids, station_ids)
    assert telescope.array.shape == (num_stations, 3)


def test_telescope_invalid_array_shape():
    """Test that Telescope raises error for invalid array shape."""
    num_stations = 4
    diameter = 10.0
    invalid_array = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [0.0, 1.0],
            [1.0, 1.0],
        ]
    )  # Invalid shape (4,2) instead of (4,3)
    expected_message = re.escape(
        f"Array shape must be ({num_stations}, 3), got {invalid_array.shape!r}"
    )
    with pytest.raises(
        ValueError,
        match=expected_message,
    ):
        Telescope(
            name="InvalidArray",
            num_stations=num_stations,
            array=invalid_array,
            diameter=diameter,
        )


def test_telescope_invalid_station_ids_shape():
    """Test that Telescope raises error for invalid station_ids shape."""
    num_stations = 4
    diameter = 10.0
    invalid_station_ids = np.array(
        ["STA001", "STA002"]
    )  # Invalid shape (2,) instead of (4,)
    expected_message = re.escape(
        f"station_ids shape must be ({num_stations},), got {invalid_station_ids.shape!r}"
    )
    with pytest.raises(
        ValueError,
        match=expected_message,
    ):
        Telescope(
            name="InvalidIDs",
            num_stations=num_stations,
            station_ids=invalid_station_ids,
            diameter=diameter,
        )


def test_telescope_array_determinism():
    """Test that the array configuration is deterministic given the same seed."""
    spec1 = TelescopeSpec(num_stations=50, diameter=30.0, seed=123)
    telescope1 = Telescope.from_spec(spec1, name="DeterministicArray")
    spec2 = TelescopeSpec(num_stations=50, diameter=30.0, seed=123)
    telescope2 = Telescope.from_spec(spec2, name="DeterministicArray")
    assert telescope1.array is not None
    assert telescope2.array is not None
    np.testing.assert_array_equal(telescope1.array, telescope2.array)


def test_telescope_array_variability():
    """Test that different seeds produce different array configurations."""
    spec1 = TelescopeSpec(num_stations=50, diameter=30.0, seed=123)
    telescope1 = Telescope.from_spec(spec1, name="VariableArray")

    spec2 = TelescopeSpec(num_stations=50, diameter=30.0, seed=456)
    telescope2 = Telescope.from_spec(spec2, name="VariableArray")

    assert telescope1.array is not None
    assert telescope2.array is not None
    assert not np.array_equal(telescope1.array, telescope2.array)


def test_telescope_get_angles(small_telescope, rng):
    """Test that _get_angles returns an array of the correct length and values within the expected range."""
    angles = small_telescope._get_angles(rng)
    assert len(angles) == 10
    assert (angles >= 0).all() and (angles <= 2 * np.pi).all()


def test_telescope_get_radii(small_telescope, rng):
    """Test that _get_radii returns an array of the correct length and values within the expected range."""
    radii = small_telescope._get_radii(rng)
    assert len(radii) == 10
    assert (radii >= 0).all() and (radii <= small_telescope.diameter / 2).all()


def test_telescope_compute_coordinates():
    """Test that _compute_coordinates returns arrays of the correct length."""
    angles = np.array([0.1] * 10)
    radii = np.array([5.0] * 10)
    x, y, z = _compute_coordinates(angles, radii)
    assert len(x) == 10
    assert len(y) == 10
    assert len(z) == 10
