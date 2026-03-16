"""Tests for Imager class."""

from starbox.image.imager import Imager
import pytest
import numpy as np
from starbox.visibility import VisibilitySet


@pytest.mark.parametrize(
    "grid_size",
    [
        128,
        256,
        512,
    ],
)
def test_imager_image_shape(grid_size, visibility_set):
    """Test that the image method returns an array of expected shape."""
    imager = Imager()
    imager.grid_size = grid_size
    image = imager.image(visibilities=visibility_set)
    assert image.shape == (grid_size, grid_size)


def test_imager_fft_output_is_real_and_finite():
    """Test that the ifft method returns finite real-valued image data."""
    imager = Imager()
    gridded_visibilities = np.ones((imager.grid_size, imager.grid_size), dtype=complex)
    image = imager.ifft(gridded_visibilities)
    assert np.isrealobj(image)
    assert np.isfinite(image).all()


def test_imager_grid_output_shape(visibility_set):
    """Test that the grid method returns an array of expected shape."""
    imager = Imager()
    gridded_visibilities = imager.grid(visibilities=visibility_set)
    assert gridded_visibilities.shape == (imager.grid_size, imager.grid_size)


def test_imager_grid_hermitian_symmetry(visibility_set):
    """Test that the grid method produces Hermitian symmetric output."""
    imager = Imager()
    gridded_visibilities = imager.grid(visibilities=visibility_set)
    flipped_conj = np.conj(np.flip(np.flip(gridded_visibilities, axis=0), axis=1))
    assert np.allclose(gridded_visibilities, flipped_conj, atol=1e-12, rtol=0.0)


def test_imager_grid_accumulates_visibilities(visibility_set):
    """Test that the grid method accumulates visibilities at the correct locations."""
    imager = Imager()
    gridded_visibilities = imager.grid(visibilities=visibility_set)

    # For this test, we can check that the maximum value in the grid is greater than zero,
    # which indicates that visibilities have been accumulated. A more detailed test would
    # require knowledge of the expected grid values based on the input visibilities.
    assert np.max(np.abs(gridded_visibilities)) > 0


def test_imager_grid_uses_all_channels():
    """Grid should include contributions from channels beyond channel 0."""
    imager = Imager(grid_size=64)
    visibilities = VisibilitySet(
        vis=np.array([[[0.0 + 0.0j, 1.0 + 0.0j]]]),  # only channel 1 has signal
        uvw_m=np.array([[[100.0, 50.0, 0.0]]]),
        station1=np.array([0]),
        station2=np.array([1]),
        times_mjd=np.array([59000.0]),
        freqs_hz=np.array([1.0e8, 2.0e8]),
        weights=np.ones((1, 1, 2)),
    )

    gridded_visibilities = imager.grid(visibilities=visibilities)
    assert np.max(np.abs(gridded_visibilities)) > 0.0


def test_imager_outside_fov():
    """Test that visibilities outside the FOV are not gridded."""
    imager = Imager(grid_size=64, fov_deg=1.0)
    visibilities = VisibilitySet(
        vis=np.array([[[1.0 + 0.0j]]]),
        uvw_m=np.array([[[1e6, 1e6, 0.0]]]),  # Very large UVW coordinates
        station1=np.array([0]),
        station2=np.array([1]),
        times_mjd=np.array([59000.0]),
        freqs_hz=np.array([1.0e8]),
        weights=np.ones((1, 1, 1)),
    )

    gridded_visibilities = imager.grid(visibilities=visibilities)
    assert np.allclose(gridded_visibilities, 0.0, atol=1e-12, rtol=0.0)
