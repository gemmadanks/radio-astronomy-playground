"""Tests for the direction cosines calculations."""

import numpy as np
from starbox.geometry.lmn import (
    calculate_lmn,
)


def test_calculate_lmn_known_case():
    """Test a known case where the source is at RA=0, Dec=0, and the phase center is also at RA=0, Dec=0."""
    ra_dec_rad = (0.0, 0.0)
    phase_centre_rad = (0.0, 0.0)

    l_dir, m_dir, n_dir = calculate_lmn(ra_dec_rad, phase_centre_rad)

    # Expect l=0, m=0, n=1
    assert l_dir == 0.0
    assert m_dir == 0.0
    assert n_dir == 1.0

def test_calculate_lmn_known_case_offset():
    """Test a known case where the source is at RA=0, Dec=0, and the phase center is at RA=0, Dec=90 degrees."""
    ra_dec_rad = (0.0, 0.0)
    phase_centre_rad = (0.0, np.pi / 2)

    l_dir, m_dir, n_dir = calculate_lmn(ra_dec_rad, phase_centre_rad)

    # Expect l=0, m=-1, n=0
    np.testing.assert_allclose(l_dir, 0.0, atol=1e-12, rtol=0.0)
    np.testing.assert_allclose(m_dir, -1.0, atol=1e-12, rtol=0.0)
    np.testing.assert_allclose(n_dir, 0.0, atol=1e-12, rtol=0.0)

def test_calculate_lmn_known_case_ra_offset():
    """Test a known case where the source is at RA=90 degrees, Dec=0, and the phase center is at RA=0, Dec=0."""
    ra_dec_rad = (np.pi / 2, 0.0)
    phase_centre_rad = (0.0, 0.0)

    l_dir, m_dir, n_dir = calculate_lmn(ra_dec_rad, phase_centre_rad)

    # Expect l=1, m=0, n=0
    np.testing.assert_allclose(l_dir, 1.0, atol=1e-12, rtol=0.0)
    np.testing.assert_allclose(m_dir, 0.0, atol=1e-12, rtol=0.0)
    np.testing.assert_allclose(n_dir, 0.0, atol=1e-12, rtol=0.0)

def test_calculate_lmn_known_case_dec_offset():
    """Test a known case where the source is at RA=0, Dec=90 degrees, and the phase center is at RA=0, Dec=0."""
    ra_dec_rad = (0.0, np.pi / 2)
    phase_centre_rad = (0.0, 0.0)

    l_dir, m_dir, n_dir = calculate_lmn(ra_dec_rad, phase_centre_rad)

    # Expect l=0, m=1, n=0
    np.testing.assert_allclose(l_dir, 0.0, atol=1e-12, rtol=0.0)
    np.testing.assert_allclose(m_dir, 1.0, atol=1e-12, rtol=0.0)
    np.testing.assert_allclose(n_dir, 0.0, atol=1e-12, rtol=0.0)
