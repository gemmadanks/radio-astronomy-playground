"""Class for handling observation parameters."""

from dataclasses import dataclass, field
import numpy as np


@dataclass(slots=True)
class Observation:
    """Observation configuration and derived sampling grids."""

    start_time: float
    observation_length: float
    num_timesteps: int
    start_frequency: float
    num_channels: int
    total_bandwidth: float

    # Derived fields (initialized in __post_init__)
    channel_width: float = field(init=False)

    # Lazy cached arrays
    _times: np.ndarray | None = field(default=None, init=False, repr=False)
    _frequencies: np.ndarray | None = field(default=None, init=False, repr=False)

    def __post_init__(self):
        if self.num_channels <= 0:
            raise ValueError(
                f"num_channels must be a positive integer, got {self.num_channels!r}"
            )

        if self.num_timesteps <= 0:
            raise ValueError(
                f"num_timesteps must be a positive integer, got {self.num_timesteps!r}"
            )

        self.channel_width = self.total_bandwidth / self.num_channels

    @property
    def times(self) -> np.ndarray:
        """Return time samples for the observation."""
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
        """Return frequency channels for the observation."""
        if self._frequencies is None:
            self._frequencies = np.array(
                [
                    self.start_frequency + i * self.channel_width
                    for i in range(self.num_channels)
                ]
            )
        return self._frequencies
