"""Functions for handling prediction of visibilities."""

import numpy as np


def predict_visibilities(telescope, skymodel, observation):
    """Predict visibilities given a telescope, sky model, and observation."""

    # Placeholder implementation: return zeros
    num_stations = telescope.num_stations
    num_times = len(observation.times)
    num_channels = len(observation.frequencies)
    num_baselines = num_stations * (num_stations - 1) // 2

    visibilities = np.zeros((num_times, num_baselines, num_channels), dtype=complex)
    return visibilities
