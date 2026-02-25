"""Module for functions related to direction cosines calculations."""

import numpy as np

def calculate_lmn(
    ra_dec_rad: tuple[float, float],
    phase_centre_rad: tuple[float, float],
) -> tuple[float, float, float]:
    """Calculate the direction cosines (l, m, n) for a source given its RA and Dec and the phase centre's RA and Dec.

    Args:
        ra_dec_rad: Right ascension and declination of the source in radians.
        phase_centre_rad: Right ascension and declination of the phase centre in radians.
    Returns:
        A tuple (l, m, n) representing the direction cosines of the source relative to the phase centre.
    """
    ra, dec = ra_dec_rad
    ra0, dec0 = phase_centre_rad

    l_dir = np.cos(dec) * np.sin(ra - ra0)
    m_dir = np.cos(dec0) * np.sin(dec) - np.sin(dec0) * np.cos(dec) * np.cos(ra - ra0)
    n_dir = np.sin(dec0) * np.sin(dec) + np.cos(dec0) * np.cos(dec) * np.cos(ra - ra0)

    return l_dir, m_dir, n_dir
