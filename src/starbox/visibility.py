"""Data class for visibility set."""

from dataclasses import dataclass
import numpy as np


@dataclass
class VisibilitySet:
    """A data class representing a set of visibilities.

    Attributes:
        vis: Complex visibilities with shape (time, baseline, chan).
        uvw_m: UVW coordinates in meters with shape (time, baseline, 3).
        station1: Indices of the first station for each baseline.
        station2: Indices of the second station for each baseline.
        times_mjd: Times of the observations in Modified Julian Date.
        freqs_hz: Frequencies of the channels in Hz.
        weights: Weights for each visibility with shape (time, baseline, chan).
    """

    vis: np.ndarray  # (time, baseline, chan)
    uvw_m: np.ndarray  # (time, baseline, 3)
    station1: np.ndarray  # (baseline,)
    station2: np.ndarray  # (baseline,)
    times_mjd: np.ndarray  # (time,)
    freqs_hz: np.ndarray  # (chan,)
    weights: np.ndarray  # (time, baseline, chan)
