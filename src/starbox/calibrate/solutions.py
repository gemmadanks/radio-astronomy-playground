"""Class for handling calibration solutions."""

from dataclasses import dataclass
from starbox.visibility import VisibilitySet
import numpy as np


@dataclass(slots=True)
class Solutions:
    """Class for handling calibration solutions.

    Attributes:
        station_phase_gains: Phase gains for each station.
    """

    station_phase_gains: np.ndarray

    def apply(self, visibilities: VisibilitySet) -> VisibilitySet:
        """Apply calibration solutions to visibilities."""

        # Placeholder implementation: return visibilities unchanged
        return visibilities
