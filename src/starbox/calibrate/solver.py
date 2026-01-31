"""Class for handling calibration solving tasks."""

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

        # Default: solve per timestep / per channel
        tbin = self.config.solint or 1

        n_time_bins = int(np.ceil(n_timesteps / tbin))
        n_freq_bins = int(np.ceil(n_channels / 1))

        # Just return unity gains (phase = 0)
        gains = np.ones(
            (n_time_bins, n_freq_bins, n_stations),
            dtype=np.complex64,
        )
        return Solutions(station_phase_gains=gains)
