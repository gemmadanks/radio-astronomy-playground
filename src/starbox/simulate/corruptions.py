"""A class for simulating corruptions."""

import numpy as np

from starbox.visibility import VisibilitySet


class Corruptions:
    """A class representing corruptions to apply to a signal.

    Attributes:
        rms_noise: The RMS noise level to add to the visibilities.
        station_phase_gain: Phase gain errors for each station.
    """

    def __init__(self, seed: int = 42):
        """Initialize the Corruptions with no corruptions."""
        self.rng = np.random.default_rng(seed)
        self.rms_noise = None
        self.sigma = None
        self.station_phase_gain = None

    def add_noise(self, rms_noise: float = 1.0):
        """Add Gaussian noise corruption."""
        self.rms_noise = rms_noise
        self.sigma = rms_noise / np.sqrt(2)

    def add_station_phase_gain(self, station_phase_gain):
        """Add station phase gain corruption."""
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
        if self.station_phase_gain is not None:
            # Placeholder for station phase gain corruption
            pass

        if self.rms_noise is not None:
            noise_real = self.rng.normal(
                scale=self.sigma, size=corrupted_visibility_set.vis.shape
            )
            noise_imag = self.rng.normal(
                scale=self.sigma, size=corrupted_visibility_set.vis.shape
            )
            noise = noise_real + 1j * noise_imag
            corrupted_visibility_set.vis += noise

        return corrupted_visibility_set
