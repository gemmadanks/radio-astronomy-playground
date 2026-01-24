"""Tests for plotting functions."""

from starbox.simulate.skymodel import SkyModel
from starbox.simulate.telescope import Telescope
from starbox.viz import plot

import numpy as np


def test_plot_skymodel():
    """Test that the plot method of SkyModel works without errors."""
    skymodel = SkyModel(name="TestModel", num_sources=20, seed=42)
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
