"""Tests for plotting functions."""

from starbox.simulate.skymodel import SkyModel
from starbox.simulate.telescope import Telescope
from starbox.viz import plot

import numpy as np


def test_skymodel_plot():
    """Test that the plot method of SkyModel works without errors."""
    skymodel = SkyModel(name="TestModel", num_sources=20, seed=42)
    plot.sky_model(skymodel)


def test_telescope_plot():
    """Test that the plot method of Telescope works without errors."""
    telescope = Telescope(name="PlotArray", num_stations=20, diameter=50.0, seed=42)
    plot.array_configuration(telescope)


def test_image_plot():
    """Test that the image plotting function works without errors."""
    # Create a mock image
    image_data = np.random.rand(100, 100)
    plot.image(image_data, title="Image Test")


def test_uv_coverage_plot():
    """Test that the UV coverage plotting function works without errors."""
    # Create mock UVW coordinates
    u = np.random.rand(100) * 1000
    v = np.random.rand(100) * 1000
    w = np.random.rand(100) * 1000
    uvw = np.column_stack((u, v, w))
    plot.uv_coverage(uvw, title="UV Coverage Test")
