"""Class for handling observation parameters."""

import numpy as np


class Observation:
    """Class for handling observation parameters."""

    def __init__(
        self,
        start_time: float,
        observation_length: float,
        num_timesteps: int,
        start_frequency: float,
        num_channels: int,
        total_bandwidth: float,
    ):
        """Initialize the Observation with given parameters."""
        self.start_time = start_time
        self.observation_length = observation_length
        self.num_timesteps = num_timesteps
        self.start_frequency = start_frequency
        self.num_channels = num_channels
        self.total_bandwidth = total_bandwidth
        self.channel_width = total_bandwidth / num_channels if num_channels > 0 else 0.0
        # Lazily computed, cached values
        self._times = None
        self._frequencies = None

    @property
    def times(self) -> np.ndarray:
        """Generate an array of time steps for the observation.

        The returned array contains ``num_timesteps`` samples. For
        ``num_timesteps > 1``, the samples are linearly spaced from
        ``start_time`` to ``start_time + observation_length`` inclusive,
        with a fixed timestep of
        ``observation_length / (num_timesteps - 1)``. For
        ``num_timesteps == 1``, the array contains only ``start_time``.
        """
        if self._times is None:
            if self.num_timesteps > 1:
                timestep = self.observation_length / (self.num_timesteps - 1)
                self._times = np.array(
                    [self.start_time + i * timestep for i in range(self.num_timesteps)]
                )
            else:
                self._times = np.array([self.start_time])
        return self._times

    @property
    def frequencies(self) -> np.ndarray:
        """Generate an array of frequency channels for the observation."""
        if self._frequencies is None:
            self._frequencies = np.array(
                [
                    self.start_frequency + i * self.channel_width
                    for i in range(self.num_channels)
                ]
            )
        return self._frequencies
