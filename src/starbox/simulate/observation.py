"""Class for handling observation parameters."""

import numpy as np

from astropy.time import Time
from astropy.utils import iers

from starbox.config.observation import ObservationConfig
import math


class Observation:
    """Observation configuration and derived sampling grids."""

    def __init__(self, config: ObservationConfig):
        self.config = config
        self.channel_width = self.config.total_bandwidth / self.config.num_channels
        self.times_mjd = None
        self.frequencies_hz = None

        self._get_times()
        self._get_frequencies()

    @property
    def phase_centre_rad(self) -> tuple[float, float]:
        """Return the phase center in radians."""
        ra_rad = math.radians(self.config.phase_center_ra)
        dec_rad = math.radians(self.config.phase_center_dec)
        return ra_rad, dec_rad

    @property
    def pointing_center_rad(self) -> tuple[float, float]:
        """Return the pointing center in radians."""
        ra_rad = math.radians(self.config.pointing_center_ra)
        dec_rad = math.radians(self.config.pointing_center_dec)
        return ra_rad, dec_rad

    @property
    def gmst_rad(self) -> np.array:
        """Return the times converted to Greenwich mean sidereal time."""
        iers.conf.auto_download = False  # avoid network calls
        times = Time(self.times_mjd, format="mjd", scale="utc")
        return times.sidereal_time("mean", "greenwich").rad

    def _get_times(self) -> None:
        """Return time samples for the observation."""
        if self.config.num_timesteps > 1:
            timestep = self.config.observation_length / (self.config.num_timesteps - 1)
            self.times_mjd = np.array(
                [
                    self.config.start_time + i * timestep
                    for i in range(self.config.num_timesteps)
                ]
            )
        else:
            self.times_mjd = np.array([self.config.start_time])

    def _get_frequencies(self) -> None:
        """Return frequency channels for the observation."""
        self.frequencies_hz = np.array(
            [
                self.config.start_frequency + i * self.channel_width
                for i in range(self.config.num_channels)
            ]
        )
