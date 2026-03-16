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


def test_imager_with_negative_fov_raises_value_error():
    """Test that initializing Imager with negative fov_deg raises ValueError."""
    with pytest.raises(ValueError, match="fov_deg must be positive"):
        Imager(fov_deg=-1.0)


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
    grid_size = imager.grid_size
    half = grid_size // 2
    # For a grid with DC located at (half, half), Hermitian symmetry implies
    # V[i, j] = conj(V[(2*half - i) % N, (2*half - j) % N]).
    ii, jj = np.indices(gridded_visibilities.shape)
    sym_ii = (2 * half - ii) % grid_size
    sym_jj = (2 * half - jj) % grid_size
    flipped_conj = np.conj(gridded_visibilities[sym_ii, sym_jj])
    assert np.allclose(gridded_visibilities, flipped_conj, atol=1e-12, rtol=0.0)


def test_imager_grid_hermitian_symmetry_does_not_double_count(visibility_set):
    """Test that the grid method does not double-count samples whose symmetric pixel is the same."""
    imager = Imager(grid_size=64, fov_deg=1.0)
    visibilities = VisibilitySet(
        vis=np.array([[[1.0 + 0.0j]]]),
        uvw_m=np.array([[[0.0, 0.0, 0.0]]]),  # UVW coordinates at the center
        station1=np.array([0]),
        station2=np.array([1]),
        times_mjd=np.array([59000.0]),
        freqs_hz=np.array([1.0e8]),
        weights=np.ones((1, 1, 1)),
    )
    gridded_visibilities = imager.grid(visibilities=visibilities)
    # The central pixel should have the value of the visibility, and there should be no other contributions
    assert np.isclose(gridded_visibilities[32, 32], 1.0 + 0.0j)
    assert np.isclose(gridded_visibilities.sum(), 1.0 + 0.0j)


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
