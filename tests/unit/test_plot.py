"""Tests for plotting functions."""

from starbox.viz import plot

import numpy as np
import pytest

import plotly.io as pio


@pytest.fixture(scope="session", autouse=True)
def configure_plotly_for_tests():
    """Configure Plotly to not open browser during tests."""
    # Set renderer to 'json' or 'png' instead of 'browser'
    pio.renderers.default = "json"


def test_plot_skymodel(skymodel):
    """Test that the plot method of SkyModel works without errors."""
    plot.plot_sky_model(skymodel)


def test_plot_telescope(small_telescope):
    """Test that the plot method of Telescope works without errors."""
    plot.plot_telescope(small_telescope)


def test_plot_image():
    """Test that the image plotting function works without errors."""
    # Create a mock image
    image_data = np.random.rand(100, 100)
    plot.plot_image(image_data, title="Image Test")


def test_plot_image_with_fov():
    """Test that the image plotting function plots as expected when FOV is provided."""
    # Create a mock image
    image_data = np.random.rand(100, 100)
    fov_deg = 1.0
    fig = plot.plot_image(image_data, title="Image Test With FOV", fov_deg=fov_deg)
    assert fig is not None
    # Check that coordinate arrays encode the requested FOV
    x_coords = np.array(fig.data[0].x)
    y_coords = np.array(fig.data[0].y)
    expected_range = fov_deg / 2
    assert np.isclose(x_coords[0], -expected_range)
    assert np.isclose(x_coords[-1], expected_range)
    assert np.isclose(y_coords[0], -expected_range)
    assert np.isclose(y_coords[-1], expected_range)
    assert len(x_coords) == image_data.shape[1]
    assert len(y_coords) == image_data.shape[0]


def test_plot_image_without_fov():
    """Test that the image plotting function plots as expected when FOV is not provided."""
    # Create a mock image
    image_data = np.random.rand(100, 100)
    fig = plot.plot_image(image_data, title="Image Test Without FOV")
    assert fig is not None
    assert fig.layout.yaxis.range is None
    assert fig.layout.xaxis.range is None

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
