"""Functions for handling prediction of visibilities."""

import numpy as np
from starbox.simulate.observation import Observation
from starbox.simulate.skymodel import SkyModel
from starbox.simulate.telescope import Telescope
from starbox.visibility import VisibilitySet


def predict_visibilities(
    telescope: Telescope, skymodel: SkyModel, observation: Observation
) -> VisibilitySet:
    """Predict visibilities given a telescope, sky model, and observation."""

    # Placeholder implementation: return zeros
    num_stations = telescope.num_stations
    num_times = len(observation.times)
    num_channels = len(observation.frequencies)
    num_baselines = num_stations * (num_stations - 1) // 2
    station1_index, station2_index = np.triu_indices(
        num_stations, k=1
    )  # strictly upper triangle

    visibilities = np.zeros((num_times, num_baselines, num_channels), dtype=complex)
    visibilities_set = VisibilitySet(
        vis=visibilities,
        uvw_m=np.zeros((num_times, num_baselines, 3)),
        station1=telescope.station_ids[station1_index],
        station2=telescope.station_ids[station2_index],
        times_mjd=observation.times,
        freqs_hz=observation.frequencies,
        weights=np.ones((num_times, num_baselines, num_channels)),
    )
    return visibilities_set
