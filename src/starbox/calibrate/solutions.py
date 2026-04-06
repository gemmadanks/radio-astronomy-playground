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
        """Apply phase-only calibration solutions to visibilities.

        The visibility corruption model is:
            V_obs = g_i * conj(g_j) * V_true
        so calibration applies the inverse factor per baseline.
        """

        n_times, _, n_channels = visibilities.vis.shape
        n_time_bins, n_freq_bins, _ = self.station_phase_gains.shape

        # Map visibility time/frequency axes to available solution bins.
        time_idx = np.minimum(
            (np.arange(n_times) * n_time_bins // max(n_times, 1)).astype(int),
            n_time_bins - 1,
        )
        freq_idx = np.minimum(
            (np.arange(n_channels) * n_freq_bins // max(n_channels, 1)).astype(int),
            n_freq_bins - 1,
        )

        gains_tf = self.station_phase_gains[time_idx[:, None], freq_idx[None, :], :]
        g1 = np.transpose(gains_tf[:, :, visibilities.station1], (0, 2, 1))
        g2 = np.transpose(gains_tf[:, :, visibilities.station2], (0, 2, 1))
        correction = g1 * np.conj(g2)

        eps = 1e-12
        calibrated_vis = np.where(
            np.abs(correction) > eps,
            visibilities.vis / correction,
            visibilities.vis,
        )

        return VisibilitySet(
            vis=calibrated_vis,
            uvw_m=np.array(visibilities.uvw_m, copy=True),
            station1=np.array(visibilities.station1, copy=True),
            station2=np.array(visibilities.station2, copy=True),
            times_mjd=np.array(visibilities.times_mjd, copy=True),
            freqs_hz=np.array(visibilities.freqs_hz, copy=True),
            weights=np.array(visibilities.weights, copy=True),
        )
