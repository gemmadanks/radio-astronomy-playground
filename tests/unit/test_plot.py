"""Tests for plotting functions."""

from starbox.viz import plot
from typing import Any, cast

import numpy as np
import pytest

import plotly.io as pio
from starbox.calibrate.solutions import Solutions


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
    image_trace = cast(Any, fig.data[0])
    x_coords = np.array(image_trace.x)
    y_coords = np.array(image_trace.y)
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
    """Test that the UV coverage plotting function returns a scatter plot."""
    # Create mock UVW coordinates
    u = np.random.rand(100) * 1000
    v = np.random.rand(100) * 1000
    w = np.random.rand(100) * 1000
    freqs_hz = np.array([100e6, 200e6], dtype=np.float64)
    # Shape (T, B, 3): T timesteps, B baselines, 3 coordinates
    uvw = np.column_stack((u, v, w)).reshape(10, 10, 3)
    fig = plot.plot_uv_coverage(uvw, freqs_hz=freqs_hz, title="UV Coverage Test")
    assert fig.layout.xaxis.title.text == "U (wavelengths)"
    assert fig.layout.yaxis.title.text == "V (wavelengths)"
    # 2 traces: grey lines + time-colored markers
    assert len(fig.data) == 2
    assert cast(Any, fig.data[0]).type == "scattergl"
    assert cast(Any, fig.data[0]).mode == "lines"
    assert cast(Any, fig.data[1]).mode == "markers"


def test_plot_uv_coverage_includes_all_samples():
    """Test UV coverage plot includes all time and baseline samples."""

    uvw = np.zeros((3, 1, 3), dtype=np.float64)
    uvw[:, 0, 0] = np.array([10.0, 20.0, 30.0])
    uvw[:, 0, 1] = np.array([0.0, 1.0, 2.0])
    freqs_hz = np.array([150e6], dtype=np.float64)

    fig = plot.plot_uv_coverage(uvw, freqs_hz=freqs_hz)

    # 2 traces: lines + markers; 3 timesteps × 1 baseline × 2 = 6 marker points
    assert len(fig.data) == 2
    x_all = np.array(cast(Any, fig.data[1]).x)
    assert x_all.size == 6
    # mirrored half should negate positive half
    np.testing.assert_allclose(x_all[3:], -x_all[:3])


def test_plot_uv_coverage_visibility_set(visibility_set):
    """Test that the UV coverage plotting function works with a VisibilitySet."""
    fig = plot.plot_uv_coverage(
        visibility_set.uvw_m,
        title="UV Coverage Test with VisibilitySet",
        freqs_hz=visibility_set.freqs_hz,
    )
    assert fig.layout.xaxis.title.text == "U (wavelengths)"
    assert fig.layout.yaxis.title.text == "V (wavelengths)"


def test_plot_uv_coverage_converts_to_wavelengths_with_freqs():
    """Test UV conversion from meters to wavelengths uses mean frequency."""

    uvw = np.zeros((1, 1, 3), dtype=np.float64)
    uvw[0, 0, 0] = 1.0  # 1 m in u
    freqs_hz = np.array([100e6, 200e6], dtype=np.float64)

    fig = plot.plot_uv_coverage(uvw, freqs_hz=freqs_hz)
    # markers trace is data[1]; 1 timestep × 1 baseline × 2 = 2 points
    x_all = np.array(cast(Any, fig.data[1]).x)
    y_all = np.array(cast(Any, fig.data[1]).y)

    c_m_per_s = 299_792_458.0
    wavelength_m = c_m_per_s / np.mean(freqs_hz)
    expected_u_lambda = 1.0 / wavelength_m

    assert x_all.size == 2
    assert y_all.size == 2
    assert np.isclose(x_all[0], expected_u_lambda)
    assert np.isclose(y_all[0], 0.0)
    assert np.isclose(x_all[1], -expected_u_lambda)  # mirrored
    assert np.isclose(y_all[1], 0.0)


def test_plot_uv_coverage_mirrors_samples_about_origin():
    """UV coverage should include the mirrored negative coordinates."""

    uvw = np.zeros((2, 1, 3), dtype=np.float64)
    uvw[:, 0, 0] = np.array([1.0, 2.0])
    uvw[:, 0, 1] = np.array([3.0, 4.0])
    freqs_hz = np.array([299_792_458.0], dtype=np.float64)

    fig = plot.plot_uv_coverage(uvw, freqs_hz=freqs_hz)

    # markers trace is data[1]; 2 timesteps × 1 baseline × 2 = 4 points
    x_all = np.array(cast(Any, fig.data[1]).x)
    y_all = np.array(cast(Any, fig.data[1]).y)

    assert x_all.size == 4
    assert y_all.size == 4
    # second half (mirrored) should negate first half (positive)
    np.testing.assert_allclose(x_all[2:], -x_all[:2])
    np.testing.assert_allclose(y_all[2:], -y_all[:2])


def test_plot_gains(solutions):
    """Test that the gain plotting function works without errors."""
    plot.plot_gains(solutions)


def test_plot_gains_shows_phase_in_degrees():
    """Test that the gains plot displays phase rather than the real component."""

    phase_deg = 90.0
    gains = np.ones((1, 1, 2), dtype=np.complex64)
    gains[0, 0, 1] = np.exp(1j * np.deg2rad(phase_deg))

    fig = plot.plot_gains(Solutions(station_phase_gains=gains), station_index=1)

    z = np.array(cast(Any, fig.data[0]).z)
    assert np.isclose(z[0, 0], phase_deg)
    assert len(fig.frames) == 0
