"""Data class for visibility set."""

from dataclasses import dataclass
import numpy as np


@dataclass
class VisibilitySet:
    vis: np.ndarray  # (time, baseline, chan)
    uvw_m: np.ndarray  # (time, baseline, 3)
    ant1: np.ndarray  # (baseline,)
    ant2: np.ndarray  # (baseline,)
    times_mjd: np.ndarray  # (time,)
    freqs_hz: np.ndarray  # (chan,)
    weights: np.ndarray | None = None
