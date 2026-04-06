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
        self.phase_time_correlation = self.config.phase_time_correlation
        self.phase_frequency_correlation = self.config.phase_frequency_correlation

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
        """Sample station phase gains in degrees with AR(1) correlations.

        A separable AR(1) process is applied along time and frequency.
        For each axis, the recursion is:
            x_t = rho * x_{t-1} + sqrt(1 - rho^2) * eps_t,
        where eps_t ~ N(0, 1). Larger ``rho`` gives smoother drifts, while
        smaller ``rho`` gives faster variation.

        Use ``phase_time_correlation=0.0`` and
        ``phase_frequency_correlation=0.0`` to force white phase noise
        (independent samples across time and channel).

        The sampled non-reference stations are rescaled so their RMS phase
        matches ``rms_phase_gain`` (in degrees). The reference station is
        pinned to zero phase.
        """
        white = self.rng.normal(
            loc=0.0,
            scale=1.0,
            size=(num_times, num_channels, num_stations),
        )

        # Create realistic smooth phase evolution by applying AR(1) correlation
        # first along time and then along frequency for each station.
        phi = np.empty_like(white)
        for station in range(num_stations):
            station_phi = self._apply_ar1(
                white[:, :, station],
                rho=self.phase_time_correlation,
                axis=0,
            )
            station_phi = self._apply_ar1(
                station_phi,
                rho=self.phase_frequency_correlation,
                axis=1,
            )
            phi[:, :, station] = station_phi

        # Scale to requested per-station RMS in degrees for non-reference stations.
        # (Reference station is pinned to zero below.)
        if num_stations > 1:
            current_rms = np.sqrt(np.mean(phi[:, :, 1:] ** 2, axis=(0, 1)))
            nonzero_rms = current_rms > 0.0
            if np.any(nonzero_rms):
                phi_nonref = phi[:, :, 1:]
                phi_nonref[:, :, nonzero_rms] *= (
                    self.rms_phase_gain / current_rms[nonzero_rms]
                )
                phi[:, :, 1:] = phi_nonref

        # Reference station to have zero phase gain at all times/frequencies
        ref_station = 0
        phi[..., ref_station] = 0.0
        station_phase_gains = np.exp(1j * np.deg2rad(phi))

        return station_phase_gains

    @staticmethod
    def _apply_ar1(samples: np.ndarray, rho: float, axis: int) -> np.ndarray:
        """Apply an AR(1) filter along a given axis while preserving shape."""
        if samples.shape[axis] <= 1:
            return np.array(samples, copy=True)

        moved = np.moveaxis(samples, axis, 0)
        out = np.empty_like(moved)

        out[0] = moved[0]
        innovation_scale = np.sqrt(max(1.0 - rho * rho, 0.0))
        for idx in range(1, moved.shape[0]):
            out[idx] = rho * out[idx - 1] + innovation_scale * moved[idx]

        return np.moveaxis(out, 0, axis)

    def _apply_noise(self, visibility_set: VisibilitySet) -> VisibilitySet:
        """Apply only the noise corruption to the given visibilities."""
        noise_real = self.rng.normal(scale=self.sigma, size=visibility_set.vis.shape)
        noise_imag = self.rng.normal(scale=self.sigma, size=visibility_set.vis.shape)
        noise = noise_real + 1j * noise_imag
        visibility_set.vis += noise

        return visibility_set
