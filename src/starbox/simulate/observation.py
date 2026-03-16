"""Class for handling observation parameters."""

import numpy as np
import numpy.typing as npt

from astropy.time import Time
from astropy.utils import iers

from starbox.config.observation import ObservationConfig
import math


class Observation:
    """Observation configuration and derived sampling grids."""

    def __init__(self, config: ObservationConfig):
        self.config = config
        self.channel_width = self.config.total_bandwidth / self.config.num_channels
        self._get_times()
        self.num_times = len(self.times_mjd)
        self._get_frequencies()
        self.num_channels = len(self.frequencies_hz)

    @property
    def phase_centre_rad(self) -> tuple[float, float]:
        """Return the phase centre in radians."""
        ra_rad = math.radians(self.config.phase_centre_ra)
        dec_rad = math.radians(self.config.phase_centre_dec)
        return ra_rad, dec_rad

    @property
    def pointing_centre_rad(self) -> tuple[float, float]:
        """Return the pointing centre in radians."""
        ra_rad = math.radians(self.config.pointing_centre_ra)
        dec_rad = math.radians(self.config.pointing_centre_dec)
        return ra_rad, dec_rad

    @property
    def gmst_rad(self) -> npt.NDArray[np.float64]:
        """Return the times converted to Greenwich mean sidereal time."""
        # Avoid mutating global Astropy IERS configuration permanently by
        # using a temporary config context while computing sidereal times.
        with iers.conf.set_temp("auto_download", False):
            times = Time(self.times_mjd, format="mjd", scale="utc")
            return np.asarray(
                times.sidereal_time("mean", "greenwich").rad,
                dtype=np.float64,
            )

    def _get_times(self) -> None:
        """Return time samples for the observation."""
        if self.config.num_timesteps > 1:
            timestep_seconds = self.config.observation_length / (
                self.config.num_timesteps - 1
            )
            timestep_mjd = timestep_seconds / 86_400.0
            self.times_mjd = np.array(
                [
                    self.config.start_time_mjd + i * timestep_mjd
                    for i in range(self.config.num_timesteps)
                ]
            )
        else:
            self.times_mjd = np.array([self.config.start_time_mjd])

    def _get_frequencies(self) -> None:
        """Return frequency channels for the observation."""
        self.frequencies_hz = np.array(
            [
                self.config.start_frequency + i * self.channel_width
                for i in range(self.config.num_channels)
            ]
        )
