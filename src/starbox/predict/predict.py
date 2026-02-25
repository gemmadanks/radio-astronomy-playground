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

    visibilities = np.zeros(
        (observation.num_times, telescope.num_baselines, observation.num_channels),
        dtype=np.complex128,
    )
    inv_wavelength_m = observation.frequencies_hz / SPEED_OF_LIGHT
    u_m = uvw_m[:, :, 0]
    v_m = uvw_m[:, :, 1]

    for ra_rad, dec_rad, flux in zip(*skymodel.as_arrays_rad()):
        l_dir, m_dir, _ = calculate_lmn(
            ra_dec_rad=(ra_rad, dec_rad), phase_centre_rad=observation.phase_centre_rad
        )
        phase_cycles = (
            u_m[:, :, np.newaxis] * l_dir + v_m[:, :, np.newaxis] * m_dir
        ) * inv_wavelength_m[np.newaxis, np.newaxis, :]
        visibilities += flux * np.exp(-2j * np.pi * phase_cycles)

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
