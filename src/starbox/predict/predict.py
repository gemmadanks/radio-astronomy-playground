"""Functions for handling prediction of visibilities."""

import numpy as np
from starbox.constants import SPEED_OF_LIGHT
from starbox.geometry.lmn import calculate_lmn
from starbox.geometry.uvw import calculate_uvw
from starbox.simulate.observation import Observation
from starbox.simulate.skymodel import SkyModel
from starbox.simulate.telescope import Telescope
from starbox.visibility import VisibilitySet


def predict_visibilities(
    telescope: Telescope, skymodel: SkyModel, observation: Observation
) -> VisibilitySet:
    """Predict visibilities given a telescope, sky model, and observation."""

    uvw_m = calculate_uvw(
        gmst_rad=observation.gmst_rad,
        phase_centre_rad=observation.phase_centre_rad,
        baselines_ecef_m=telescope.baselines_ecef,
    )

    # Inverse wavelength for each channel (1 / meters)
    inv_wavelength_m = observation.frequencies_hz / SPEED_OF_LIGHT

    # Extract sky model parameters as arrays
    ra_arr, dec_arr, flux_arr = skymodel.as_arrays_rad()

    # Handle empty sky model: return zero visibilities
    if ra_arr.size == 0:
        visibilities = np.zeros(
            (observation.num_times, telescope.num_baselines, observation.num_channels),
            dtype=np.complex128,
        )
    else:
        # Precompute direction cosines (l, m, n-1) for all sources
        num_sources = ra_arr.size
        l_arr = np.empty(num_sources, dtype=np.float64)
        m_arr = np.empty(num_sources, dtype=np.float64)
        n_arr = np.empty(num_sources, dtype=np.float64)
        for i, (ra_rad, dec_rad) in enumerate(zip(ra_arr, dec_arr)):
            l_dir, m_dir, n_dir = calculate_lmn(
                ra_dec_rad=(ra_rad, dec_rad),
                phase_centre_rad=observation.phase_centre_rad,
            )
            l_arr[i] = l_dir
            m_arr[i] = m_dir
            n_arr[i] = n_dir

        # Direction vectors (l, m, n-1) for each source: shape (num_sources, 3)
        dir_vecs = np.stack([l_arr, m_arr, n_arr - 1.0], axis=1)

        # Project UVW coordinates onto all source direction vectors.
        # uvw_m: (num_times, num_baselines, 3)
        # dir_vecs: (num_sources, 3)
        # Result proj: (num_times, num_baselines, num_sources)
        proj = np.tensordot(uvw_m, dir_vecs, axes=([2], [1]))

        # Convert path difference (meters) to phase cycles for all channels and sources:
        # phase_cycles shape: (num_times, num_baselines, num_channels, num_sources)
        phase_cycles = (
            proj[:, :, np.newaxis, :]
            * inv_wavelength_m[np.newaxis, np.newaxis, :, np.newaxis]
        )

        # Compute complex exponentials and sum over sources weighted by flux.
        # exp_phase: (num_times, num_baselines, num_channels, num_sources)
        exp_phase = np.exp(-2j * np.pi * phase_cycles)
        # visibilities: (num_times, num_baselines, num_channels)
        visibilities = np.tensordot(exp_phase, flux_arr, axes=([3], [0]))

    station1_index, station2_index = np.triu_indices(
        telescope.num_stations, k=1
    )  # strictly upper triangle
    visibilities_set = VisibilitySet(
        vis=visibilities,
        uvw_m=uvw_m,
        station1=station1_index,
        station2=station2_index,
        times_mjd=observation.times_mjd,
        freqs_hz=observation.frequencies_hz,
        weights=np.ones(
            (observation.num_times, telescope.num_baselines, observation.num_channels)
        ),
    )
    return visibilities_set
