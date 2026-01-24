"""Test the Telescope class."""

import pytest

from starbox.simulate.telescope import Telescope, _compute_coordinates
import numpy as np


def test_telescope_initialization():
    """Test that a Telescope object initializes correctly."""
    telescope = Telescope(name="ELA", num_stations=100, diameter=50.0)
    assert telescope.name == "ELA"
    assert telescope.num_stations == 100
    assert telescope.diameter == 50.0
    assert telescope.array.shape == (100, 3)
    assert (
        telescope.station_ids == np.array([f"ELA_STN{idx:03d}" for idx in range(100)])
    ).all()


def test_telescope_repr():
    """Test the string representation of the Telescope object."""
    telescope = Telescope(name="TestArray", num_stations=20, diameter=10.0)
    repr_str = repr(telescope)
    assert "Telescope(name=TestArray, num_stations=20, diameter=10.0 m" in repr_str


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
    telescope = Telescope(
        name=name, num_stations=num_stations, diameter=diameter, seed=seed
    )
    assert telescope.rng is not None
    assert telescope.array.shape == (num_stations, 3)
    assert telescope.array.dtype == float
    assert telescope.array.max() <= diameter
    assert (
        telescope.station_ids
        == np.array([f"{name}_STN{idx:03d}" for idx in range(num_stations)])
    ).all()


def test_telescope_array_determinism():
    """Test that the array configuration is deterministic given the same seed."""
    telescope1 = Telescope(
        name="DeterministicArray", num_stations=50, diameter=30.0, seed=123
    )
    telescope2 = Telescope(
        name="DeterministicArray", num_stations=50, diameter=30.0, seed=123
    )
    assert (telescope1.array == telescope2.array).all()


def test_telescope_array_variability():
    """Test that different seeds produce different array configurations."""
    telescope1 = Telescope(
        name="VariableArray", num_stations=50, diameter=30.0, seed=123
    )
    telescope2 = Telescope(
        name="VariableArray", num_stations=50, diameter=30.0, seed=456
    )
    assert not (telescope1.array == telescope2.array).all()


def test_telescope_get_angles(small_telescope):
    """Test that _get_angles returns an array of the correct length and values within the expected range."""
    angles = small_telescope._get_angles()
    assert len(angles) == 10
    assert (angles >= 0).all() and (angles <= 2 * np.pi).all()


def test_telescope_get_radii(small_telescope):
    """Test that _get_radii returns an array of the correct length and values within the expected range."""
    radii = small_telescope._get_radii()
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


def test_telescope_reconfigure():
    """Test that reconfigure changes the array configuration."""
    telescope = Telescope(name="ReconfigArray", num_stations=30, diameter=40.0, seed=42)
    original_array = telescope.array.copy()
    telescope.reconfigure(seed=43)
    new_array = telescope.array
    assert not (original_array == new_array).all()
