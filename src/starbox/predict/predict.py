"""Functions for handling prediction of visibilities."""

import numpy as np
from starbox.visibility import VisibilitySet


def predict_visibilities(telescope, skymodel, observation):
    """Predict visibilities given a telescope, sky model, and observation."""

    # Placeholder implementation: return zeros
    num_stations = telescope.num_stations
    num_times = len(observation.times)
    num_channels = len(observation.frequencies)
    num_baselines = num_stations * (num_stations - 1) // 2

    visibilities = np.zeros((num_times, num_baselines, num_channels), dtype=complex)
    visibilities_set = VisibilitySet(
        vis=visibilities,
        uvw_m=np.zeros((num_times, num_baselines, 3)),
        station1=np.array([i for i in range(num_baselines)]),
        station2=np.array([i for i in range(num_baselines)]),
        times_mjd=observation.times,
        freqs_hz=observation.frequencies,
        weights=np.ones((num_times, num_baselines, num_channels)),
    )
    return visibilities_set
