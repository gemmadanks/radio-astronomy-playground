"""Class for handling calibration solving tasks."""

from typing import Optional

import numpy as np
from starbox.calibrate.solutions import Solutions
from starbox.config.solver import SolverConfig
from starbox.visibility import VisibilitySet


class Solver:
    """Class to handle calibration solving."""

    def __init__(self, config: SolverConfig):
        self.config = config

    def solve(
        self,
        observed_visibilities: VisibilitySet,
        model_visibilities: VisibilitySet,
        n_stations: int,
    ) -> Solutions:
        """Estimate calibration solutions from observed and model visibilities."""

        n_timesteps, _, n_channels = observed_visibilities.vis.shape
        tbin = float(self.config.solution_interval_seconds)
        n_time_bins = int(np.ceil(n_timesteps / tbin))

        gains = np.ones((n_time_bins, n_channels, n_stations), dtype=np.complex128)

        for time_bin in range(n_time_bins):
            t_start = int(time_bin * tbin)
            t_stop = min(int((time_bin + 1) * tbin), n_timesteps)
            obs_bin = observed_visibilities.vis[t_start:t_stop]
            mod_bin = model_visibilities.vis[t_start:t_stop]
            w_bin = observed_visibilities.weights[t_start:t_stop]

            for chan in range(n_channels):
                gains[time_bin, chan] = self._solve_bin_channel(
                    observed_bin=obs_bin[:, :, chan],
                    model_bin=mod_bin[:, :, chan],
                    weights_bin=w_bin[:, :, chan],
                    station1=observed_visibilities.station1,
                    station2=observed_visibilities.station2,
                    n_stations=n_stations,
                )

        return Solutions(station_phase_gains=gains.astype(np.complex64))

    def _solve_bin_channel(
        self,
        observed_bin: np.ndarray,
        model_bin: np.ndarray,
        weights_bin: np.ndarray,
        station1: np.ndarray,
        station2: np.ndarray,
        n_stations: int,
    ) -> np.ndarray:
        """Solve station phase gains for one (time-bin, channel).

        Uses a spectral phase-synchronization approach over baseline ratios,
        which is significantly faster than iterative nonlinear least squares.
        """
        eps = 1e-12

        # Robust weighted estimate of baseline phase ratios across timesteps
        valid = np.abs(model_bin) > eps
        safe_model = np.where(valid, model_bin, 1.0 + 0j)
        ratios = np.where(valid, observed_bin / safe_model, 0.0 + 0j)

        w = weights_bin * valid
        wsum = np.sum(w, axis=0)
        ratio_mean = np.sum(w * ratios, axis=0)
        ratio_mean = np.where(wsum > 0.0, ratio_mean / np.maximum(wsum, eps), 0.0 + 0j)

        # Keep only phase information (phase-only calibration)
        amp = np.abs(ratio_mean)
        phase_ratio = np.where(amp > eps, ratio_mean / amp, 0.0 + 0j)

        # Build Hermitian pairwise phase consistency matrix
        h = np.zeros((n_stations, n_stations), dtype=np.complex128)
        degree = np.zeros(n_stations, dtype=np.float64)

        for bl in range(station1.size):
            i = int(station1[bl])
            j = int(station2[bl])
            z = phase_ratio[bl]
            if z == 0.0:
                continue
            h[i, j] += z
            h[j, i] += np.conj(z)
            degree[i] += 1.0
            degree[j] += 1.0

        # Principal eigenvector gives gains up to a global phase
        eigvals, eigvecs = np.linalg.eigh(h)
        g = eigvecs[:, np.argmax(eigvals)]

        # Normalize to unit modulus and fix gauge with station 0 as reference
        g_amp = np.abs(g)
        gains = np.ones_like(g)
        nonzero = g_amp > eps
        gains[nonzero] = g[nonzero] / g_amp[nonzero]

        ref = gains[0]
        ref = ref / np.abs(ref) if np.abs(ref) > eps else 1.0 + 0j
        gains = gains / ref

        # Keep unobserved stations neutral
        gains[degree == 0.0] = 1.0 + 0j
        gains[0] = 1.0 + 0j

        return gains

    def _phases_to_gains(
        self,
        phases: np.ndarray,
        n_time_bins: int,
        n_freq_bins: int,
        n_stations: int,
    ) -> np.ndarray:
        """Convert a flat real phase vector to complex station gains.

        Station 0 is the reference and is prepended at phase=0 (gain=1+0j).
        """
        phase_free = phases.reshape((n_time_bins, n_freq_bins, n_stations - 1))
        # Prepend a zero-phase column for the reference station
        phase_all = np.pad(phase_free, ((0, 0), (0, 0), (1, 0)))
        return np.exp(1j * phase_all)

    def _residuals(
        self,
        gains,
        observed_visibilities: VisibilitySet,
        model_visibilities: VisibilitySet,
        n_stations: Optional[int] = None,
    ) -> np.ndarray:
        """Calculate residuals between observed and model visibilities given station gains.

        Accepts either:
          - A 3D complex array (time_bins, freq_bins, n_stations) passed directly from tests.
          - A 1D real phase vector from scipy.optimize.least_squares (station 0 excluded).
        Returns a real 1D vector of interleaved real/imag residuals per visibility sample.
        """
        gains_arr = np.asarray(gains)
        n_timesteps, _, n_channels = observed_visibilities.vis.shape
        tbin = float(self.config.solution_interval_seconds or 1)

        if gains_arr.ndim == 3:
            gains_3d = gains_arr
        else:
            assert n_stations is not None, "n_stations is required for 1D phase vector"
            n_time_bins = int(np.ceil(n_timesteps / tbin))
            gains_3d = self._phases_to_gains(
                gains_arr, n_time_bins, n_channels, n_stations
            )

        n_time_bins = gains_3d.shape[0]

        # Map each timestep to its solution bin — shape (n_timesteps,)
        time_bins = np.minimum(
            (np.arange(n_timesteps) / tbin).astype(int), n_time_bins - 1
        )

        # Gather per-(timestep, baseline) gains in a single vectorised index.
        # time_bins[:, None] -> (n_timesteps, 1), station[None, :] -> (1, n_baselines)
        # Advanced indices at positions 0 and 2 (non-adjacent) → result shape:
        # (n_timesteps, n_baselines, n_freq_bins)
        station1 = observed_visibilities.station1
        station2 = observed_visibilities.station2
        gain_1 = gains_3d[time_bins[:, None], :, station1[None, :]]
        gain_2 = gains_3d[time_bins[:, None], :, station2[None, :]]

        predicted = gain_1 * np.conj(gain_2) * model_visibilities.vis
        residual = observed_visibilities.vis - predicted
        sqrt_weights = np.sqrt(observed_visibilities.weights)
        weighted = sqrt_weights * residual

        # Interleave real and imaginary parts into a flat real 1D array
        weighted_arr = np.asarray(weighted, dtype=np.complex128)
        return np.stack([weighted_arr.real, weighted_arr.imag], axis=-1).ravel()
