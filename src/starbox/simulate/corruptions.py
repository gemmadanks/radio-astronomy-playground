"""A class for simulating corruptions."""

import numpy as np


class Corruptions:
    """A class representing corruptions to apply to a signal."""

    def __init__(self):
        self.rms_noise = None
        self.station_phase_gain = None

    def add_noise(self, rms_noise=1):
        self.rms_noise = rms_noise

    def add_station_phase_gain(self, station_phase_gain):
        self.station_phase_gain = station_phase_gain

    def apply(self, visibilitites):
        """Apply the corruptions to the given visibilities."""
        corrupted_visibilities = visibilitites.copy()
        if self.rms_noise is not None:
            noise = self.rms_noise * (
                np.random.randn(*visibilitites.shape)
                + 1j * np.random.randn(*visibilitites.shape)
            )
            corrupted_visibilities += noise
        if self.station_phase_gain is not None:
            # Placeholder for station phase gain corruption
            pass
        return corrupted_visibilities
