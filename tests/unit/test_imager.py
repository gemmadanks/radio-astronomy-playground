"""Tests for Imager class."""

from starbox.image.imager import Imager
import pytest
import numpy as np


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


def test_imager_fft_output_non_negative():
    """Test that the fft method returns non-negative values."""
    imager = Imager()
    gridded_visibilities = np.ones((imager.grid_size, imager.grid_size), dtype=complex)
    image = imager.fft(gridded_visibilities)
    assert (image >= 0).all()


def test_imager_grid_output_shape(visibility_set):
    """Test that the grid method returns an array of expected shape."""
    imager = Imager()
    gridded_visibilities = imager.grid(visibilities=visibility_set.vis)
    assert gridded_visibilities.shape == (imager.grid_size, imager.grid_size)
