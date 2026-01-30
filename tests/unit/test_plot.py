"""Tests for plotting functions."""

from starbox.simulate.skymodel import SkyModel
from starbox.simulate.telescope import Telescope
from starbox.viz import plot

import numpy as np

import pytest


def test_plot_skymodel(skymodel_spec):
    """Test that the plot method of SkyModel works without errors."""
    skymodel = SkyModel.from_spec(skymodel_spec)
    plot.plot_sky_model(skymodel)


def test_plot_telescope():
    """Test that the plot method of Telescope works without errors."""
    telescope = Telescope(name="PlotArray", num_stations=20, diameter=50.0, seed=42)
    plot.plot_array_configuration(telescope)


def test_plot_image():
    """Test that the image plotting function works without errors."""
    # Create a mock image
    image_data = np.random.rand(100, 100)
    plot.plot_image(image_data, title="Image Test")


def test_plot_uv_coverage():
    """Test that the UV coverage plotting function works without errors."""
    # Create mock UVW coordinates
    u = np.random.rand(100) * 1000
    v = np.random.rand(100) * 1000
    w = np.random.rand(100) * 1000
    uvw = np.column_stack((u, v, w))
    plot.plot_uv_coverage(uvw, title="UV Coverage Test")


def test_plot_gains(solutions):
    """Test that the gain plotting function works without errors."""
    plot.plot_gains(solutions)


def test_plot_telescope_array_is_none():
    """Test that plot_array_configuration raises ValueError when array is None."""
    telescope = Telescope(name="NoArray", num_stations=10, diameter=20.0)
    telescope.array = None  # Manually set array to None to simulate uninitialized state
    with pytest.raises(ValueError, match="Telescope array is not initialised."):
        plot.plot_array_configuration(telescope)
