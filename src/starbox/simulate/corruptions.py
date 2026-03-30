"""A class for simulating corruptions."""

import numpy as np

from starbox.visibility import VisibilitySet
from starbox.config.corruptions import CorruptionsConfig


class Corruptions:
    """A class representing corruptions to apply to a signal.

    Attributes:
        rms_noise: The RMS noise level to add to the visibilities.
        station_phase_gain: Phase gain errors for each station.
    """

    def __init__(self, config: CorruptionsConfig):
        self.config = config
        self.rng = np.random.default_rng(self.config.seed)
        self._add_noise()
        self._add_station_phase_gain()

    def _add_noise(self):
        """Add Gaussian noise corruption."""
        self.sigma = self.config.rms_noise / np.sqrt(2)

    def _add_station_phase_gain(self):
        """Add station phase gain corruption."""
        self.rms_phase_gain = self.config.rms_phase_gain

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
        if abs(self.rms_phase_gain) != 0.0:
            station_phase_gains = self._sample_station_phase_gains(
                num_times=visibility_set.vis.shape[0],
                num_channels=visibility_set.vis.shape[2],
                num_stations=visibility_set.num_stations,
            )
            corrupted_visibility_set = self._apply_station_phase_gain(
                corrupted_visibility_set, station_phase_gains
            )
        if abs(self.sigma) != 0.0:
            corrupted_visibility_set = self._apply_noise(corrupted_visibility_set)

        return corrupted_visibility_set

    def _apply_station_phase_gain(
        self, visibility_set: VisibilitySet, station_phase_gains: np.ndarray
    ) -> VisibilitySet:
        """Apply only the station phase gain corruption to the given visibilities."""
        if station_phase_gains.ndim == 1:
            phase_gains_1 = station_phase_gains[visibility_set.station1][
                np.newaxis, :, np.newaxis
            ]
            phase_gains_2 = station_phase_gains[visibility_set.station2][
                np.newaxis, :, np.newaxis
            ]
            visibility_set.vis *= phase_gains_1 * np.conj(phase_gains_2)
            return visibility_set

        phase_gains_1 = np.transpose(
            station_phase_gains[:, :, visibility_set.station1], (0, 2, 1)
        )
        phase_gains_2 = np.transpose(
            station_phase_gains[:, :, visibility_set.station2], (0, 2, 1)
        )
        visibility_set.vis *= phase_gains_1 * np.conj(phase_gains_2)

        return visibility_set

    def _sample_station_phase_gains(
        self, num_times: int, num_channels: int, num_stations: int
    ) -> np.ndarray:
        """Sample random phase gains for each time, channel, and station."""
        phi = self.rng.normal(
            loc=0.0,
            scale=self.rms_phase_gain,
            size=(num_times, num_channels, num_stations),
        )
        # Reference station to have zero phase gain at all times/frequencies
        ref_station = 0
        phi[..., ref_station] = 0.0
        station_phase_gains = np.exp(1j * np.deg2rad(phi))

        return station_phase_gains

    def _apply_noise(self, visibility_set: VisibilitySet) -> VisibilitySet:
        """Apply only the noise corruption to the given visibilities."""
        noise_real = self.rng.normal(scale=self.sigma, size=visibility_set.vis.shape)
        noise_imag = self.rng.normal(scale=self.sigma, size=visibility_set.vis.shape)
        noise = noise_real + 1j * noise_imag
        visibility_set.vis += noise

        return visibility_set
