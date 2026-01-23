"""A class for simulating corruptions."""

import numpy as np

from starbox.visibility import VisibilitySet


class Corruptions:
    """A class representing corruptions to apply to a signal."""

    def __init__(self):
        self.rms_noise = None
        self.station_phase_gain = None

    def add_noise(self, rms_noise: float = 1.0):
        self.rms_noise = rms_noise

    def add_station_phase_gain(self, station_phase_gain):
        self.station_phase_gain = station_phase_gain

    def apply(self, visibility_set: VisibilitySet) -> VisibilitySet:
        """Apply the corruptions to the given visibilities."""
        corrupted_visibility_set = VisibilitySet(
            vis=np.copy(visibility_set.vis),
            uvw_m=visibility_set.uvw_m,
            station1=visibility_set.station1,
            station2=visibility_set.station2,
            times_mjd=visibility_set.times_mjd,
            freqs_hz=visibility_set.freqs_hz,
            weights=visibility_set.weights,
        )
        if self.rms_noise is not None:
            noise = self.rms_noise * (
                np.random.randn(*corrupted_visibility_set.vis.shape)
                + 1j * np.random.randn(*corrupted_visibility_set.vis.shape)
            )
            corrupted_visibility_set.vis += noise
        if self.station_phase_gain is not None:
            # Placeholder for station phase gain corruption
            pass

        return corrupted_visibility_set
