"""Class for handling calibration solving tasks."""

import numpy as np
from starbox.calibrate.solutions import Solutions
from starbox.visibility import VisibilitySet
from dataclasses import dataclass


@dataclass(slots=True)
class SolverSpec:
    """Specification for the calibration solver.

    Attributes:
        solint: Solution interval in seconds.
    """

    solint: float


@dataclass(slots=True)
class Solver:
    """Class to handle calibration solving."""

    solint: float

    def __post_init__(self):
        if self.solint <= 0:
            raise ValueError("Solution interval must be positive.")

    @classmethod
    def from_spec(cls, spec: SolverSpec) -> "Solver":
        """Create a Solver instance from a SolverSpec."""
        return cls(solint=spec.solint)

    def solve(
        self,
        observed_visibilities: VisibilitySet,
        model_visibilities: VisibilitySet,
        n_stations: int,
    ) -> Solutions:
        """Estimate calibration solutions from observed and model visibilities."""

        n_timesteps, _, n_channels = observed_visibilities.vis.shape

        # Default: solve per timestep / per channel
        tbin = self.solint or 1

        n_time_bins = int(np.ceil(n_timesteps / tbin))
        n_freq_bins = int(np.ceil(n_channels / 1))

        # Just return unity gains (phase = 0)
        gains = np.ones(
            (n_time_bins, n_freq_bins, n_stations),
            dtype=np.complex64,
        )
        return Solutions(station_phase_gains=gains)
