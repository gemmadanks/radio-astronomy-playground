"""Tests for plotting functions."""

from starbox.simulate.skymodel import SkyModel
from starbox.simulate.telescope import Telescope
from starbox.viz import plot


def test_skymodel_plot():
    """Test that the plot method of SkyModel works without errors."""
    skymodel = SkyModel(name="TestModel", num_sources=20, seed=42)
    plot.sky_model(skymodel)


def test_telescope_plot():
    """Test that the plot method of Telescope works without errors."""
    telescope = Telescope(name="PlotArray", num_stations=20, diameter=50.0, seed=42)
    plot.array_configuration(telescope)
