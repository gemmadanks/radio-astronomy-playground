"""Class for handling calibration solving tasks."""

import numpy as np
from starbox.calibrate.solutions import Solutions
from starbox.config.solver import SolverConfig
from starbox.visibility import VisibilitySet

from scipy.optimize import least_squares


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
        n_freq_bins = n_channels

        # Station 0 is fixed as the phase reference; only stations 1..n_stations-1 are free.
        n_stations_free = n_stations - 1
        initial_guess = np.zeros(
            n_time_bins * n_freq_bins * n_stations_free, dtype=np.float64
        )
        result = least_squares(
            self._residuals,
            initial_guess,
            args=(observed_visibilities, model_visibilities, n_stations),
        )
        gains = self._phases_to_gains(result.x, n_time_bins, n_freq_bins, n_stations)
        return Solutions(station_phase_gains=gains.astype(np.complex64))

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
        n_stations_free = n_stations - 1
        phase_free = phases.reshape((n_time_bins, n_freq_bins, n_stations_free))
        ref = np.zeros((n_time_bins, n_freq_bins, 1))
        phase_all = np.concatenate([ref, phase_free], axis=2)
        return np.exp(1j * phase_all)

    def _residuals(
        self,
        gains,
        observed_visibilities: VisibilitySet,
        model_visibilities: VisibilitySet,
        n_stations: int = None,
    ) -> np.ndarray:
        """Calculate residuals between observed and model visibilities given station gains.

        Accepts either:
          - A 3D complex array (time_bins, freq_bins, n_stations) passed directly from tests.
          - A 1D real phase vector from scipy.optimize.least_squares (station 0 excluded).
        Returns a real 1D vector of interleaved real/imag residuals per visibility sample.
        """
        gains_arr = np.asarray(gains)

        if gains_arr.ndim == 3:
            gains_3d = gains_arr
        else:
            n_timesteps, _, n_channels = observed_visibilities.vis.shape
            tbin = float(self.config.solution_interval_seconds or 1)
            n_time_bins = int(np.ceil(n_timesteps / tbin))
            n_freq_bins = n_channels
            gains_3d = self._phases_to_gains(
                gains_arr, n_time_bins, n_freq_bins, n_stations
            )

        tbin = float(self.config.solution_interval_seconds or 1)
        n_time_bins, n_freq_bins, _ = gains_3d.shape
        residuals = []

        for t in range(observed_visibilities.vis.shape[0]):
            time_bin = min(int(t // tbin), n_time_bins - 1)
            for baseline in range(observed_visibilities.vis.shape[1]):
                station1 = int(observed_visibilities.station1[baseline])
                station2 = int(observed_visibilities.station2[baseline])
                gain_1 = gains_3d[time_bin, :, station1]
                gain_2 = gains_3d[time_bin, :, station2]
                predicted = (
                    gain_1
                    * np.conj(gain_2)
                    * model_visibilities.vis[t, baseline, :n_freq_bins]
                )
                residual = (
                    observed_visibilities.vis[t, baseline, :n_freq_bins] - predicted
                )
                weight = np.sqrt(
                    observed_visibilities.weights[t, baseline, :n_freq_bins]
                )
                weighted = weight * residual
                residuals.append(np.real(weighted))
                residuals.append(np.imag(weighted))

        return np.concatenate(residuals)
