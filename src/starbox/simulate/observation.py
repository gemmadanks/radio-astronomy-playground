"""Class for handling observation parameters."""

import numpy as np

from starbox.config.observation import ObservationConfig


class Observation:
    """Observation configuration and derived sampling grids."""

    def __init__(self, config: ObservationConfig):
        self.config = config
        self.channel_width = self.config.total_bandwidth / self.config.num_channels

        self._get_times()
        self._get_frequencies()

    def _get_times(self) -> None:
        """Return time samples for the observation."""
        if self.config.num_timesteps > 1:
            timestep = self.config.observation_length / (self.config.num_timesteps - 1)
            self.times = np.array(
                [
                    self.config.start_time + i * timestep
                    for i in range(self.config.num_timesteps)
                ]
            )
        else:
            self.times = np.array([self.config.start_time])

    def _get_frequencies(self) -> None:
        """Return frequency channels for the observation."""
        self.frequencies = np.array(
            [
                self.config.start_frequency + i * self.channel_width
                for i in range(self.config.num_channels)
            ]
        )
