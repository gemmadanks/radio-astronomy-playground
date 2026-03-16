"""Module for functions related to UVW calculations."""

import numpy as np


def calculate_uvw(
    gmst_rad: np.ndarray,
    phase_centre_rad: tuple[float, float],
    baselines_ecef_m: np.ndarray,
) -> np.ndarray:
    """Calculate UVW coordinates.

    Args:
      gmst_rad: A 1D array of Greenwich mean sidereal times in radians.
      phase_centre_rad: A tuple (ra0, dec0) representing the right ascension and declination of the phase centre in radians.
      baselines_ecef_m: A (num_baselines, 3) array of baseline vectors in ECEF coordinates (meters).

    Returns:
      uvw_m: (num_times, num_baselines, 3) array in meters.
    """

    uvw_basis = _uvw_basis_from_phase_centre(phase_centre_rad)

    num_times = gmst_rad.size
    num_baselines = baselines_ecef_m.shape[0]
    uvw_m = np.empty((num_times, num_baselines, 3), dtype=float)

    for time_index in range(num_times):
        baselines_equatorial_m = (_rot_z(gmst_rad[time_index]) @ baselines_ecef_m.T).T
        uvw_m[time_index] = (uvw_basis @ baselines_equatorial_m.T).T

    return uvw_m


def _uvw_basis_from_phase_centre(
    phase_centre_rad: tuple[float, float],
) -> np.ndarray:
    """Calculate the base UVW transformation matrix for a given phase centre.

    Args:
        phase_centre_rad: A tuple (ra0, dec0) representing the right ascension and declination of the phase centre in radians.

    Returns:
        A 3x3 numpy array representing the UVW transformation matrix.
    """
    ra0, dec0 = phase_centre_rad
    sin_ra0, cos_ra0 = np.sin(ra0), np.cos(ra0)
    sin_dec0, cos_dec0 = np.sin(dec0), np.cos(dec0)

    return np.array(
        [
            [-sin_ra0, cos_ra0, 0.0],
            [-sin_dec0 * cos_ra0, -sin_dec0 * sin_ra0, cos_dec0],
            [cos_dec0 * cos_ra0, cos_dec0 * sin_ra0, sin_dec0],
        ],
        dtype=float,
    )


def _rot_z(gmst_rad: float) -> np.ndarray:
    """Calculate the transformation matrix to rotate Greenwich mean sidereal time to the equatorial frame.

    Args:
        gmst_rad: The Greenwich mean sidereal time in radians.

    Returns:
        A 3x3 numpy array representing the rotation matrix to transform from GMST to equatorial coordinates.
    """
    sin_gmst, cos_gmst = np.sin(gmst_rad), np.cos(gmst_rad)
    return np.array(
        [[cos_gmst, sin_gmst, 0.0], [-sin_gmst, cos_gmst, 0.0], [0.0, 0.0, 1.0]],
        dtype=float,
    )
