"""Tests for geometry calculations in radio astronomy."""

import numpy as np
from starbox.geometry.uvw import (
    calculate_uvw,
    _uvw_basis_from_phase_centre,
    _rot_z,
)


def test_calculate_uvw_dimensions():
    """Test the calculate_uvw function returns correct dimensions."""
    times_gmst_rad = np.array([0.0, 1.0, 2.0])  # in radians
    baselines_ecef = np.array([[0, 0, 0], [100, 0, 0], [0, 100, 0]])  # in meters
    phase_centre_rad = (0.0, 0.0)  # in radians

    uvw_m = calculate_uvw(times_gmst_rad, phase_centre_rad, baselines_ecef)
    assert uvw_m.shape == (len(times_gmst_rad), baselines_ecef.shape[0], 3)


def test_calculate_uvw_preserves_dot_products_between_baselines():
    """
    Rotations preserve angles: dot(b1, b2) should be invariant under the transform.
    """
    rng = np.random.default_rng(2)
    baselines = rng.normal(size=(10, 3)) * 100.0
    gmst = np.array([0.0, 0.7, 1.2])
    uvw = calculate_uvw(gmst, (1.0, 0.1), baselines)

    # Compare dot products between a pair of baselines across times
    i, j = 3, 7
    dot0 = np.dot(uvw[0, i], uvw[0, j])
    dot1 = np.dot(uvw[1, i], uvw[1, j])
    dot2 = np.dot(uvw[2, i], uvw[2, j])
    np.testing.assert_allclose([dot1, dot2], [dot0, dot0], atol=1e-10, rtol=0.0)


def test_calculate_uvw_known_case_ra0_dec0_zero_gmst_zero():
    """Test a known case where the phase centre is at RA=0, Dec=0, and GMST=0."""
    gmst = np.array([0.0])
    phase_centre = (0.0, 0.0)

    # Use a single baseline with known components
    baselines = np.array([[1.0, 2.0, 3.0]])  # X=1, Y=2, Z=3
    uvw = calculate_uvw(gmst, phase_centre, baselines)

    # Expect u=2, v=3, w=1
    np.testing.assert_allclose(
        uvw[0, 0], np.array([2.0, 3.0, 1.0]), atol=1e-12, rtol=0.0
    )


def test_calculate_uvw_known_case_gmst_half_turn():
    """Test a known case where the phase centre is at RA=0, Dec=0, and GMST=pi (half turn)."""
    gmst = np.array([np.pi])
    phase_centre = (0.0, 0.0)

    baselines = np.array([[1.0, 2.0, 3.0]])
    uvw = calculate_uvw(gmst, phase_centre, baselines)

    np.testing.assert_allclose(
        uvw[0, 0], np.array([-2.0, 3.0, -1.0]), atol=1e-12, rtol=0.0
    )


def test_uvw_basis_from_phase_centre():
    """Test the _uvw_basis_from_phase_centre function with a known case."""
    phase_centre_rad = (0.0, 0.0)  # RA=0, Dec=0
    uvw_basis = _uvw_basis_from_phase_centre(phase_centre_rad)

    expected_basis = np.array(
        [
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
        ]
    )
    np.testing.assert_allclose(uvw_basis, expected_basis, atol=1e-12, rtol=0.0)


def test_rot_z():
    """Test the _rot_z function with a known case."""
    gmst_rad = np.pi / 2  # 90 degrees rotation
    rot_matrix = _rot_z(gmst_rad)

    expected_rot = np.array(
        [
            [0.0, 1.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    np.testing.assert_allclose(rot_matrix, expected_rot, atol=1e-12, rtol=0.0)
