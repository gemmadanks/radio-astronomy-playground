"""Class for handling observation parameters."""

from dataclasses import dataclass, field
import numpy as np


@dataclass
class ObservationSpec:
    """A dataclass representing the specification for an observation.

    Attributes:
        start_time: Start time of the observation in MJD.
        observation_length: Length of the observation in seconds.
        num_timesteps: Number of time steps in the observation.
        start_frequency: Starting frequency in Hz.
        num_channels: Number of frequency channels.
        total_bandwidth: Total bandwidth in Hz."""

    start_time: float
    observation_length: float
    num_timesteps: int
    start_frequency: float
    num_channels: int
    total_bandwidth: float

    def __post_init__(self):
        if self.num_channels <= 0:
            raise ValueError(
                f"num_channels must be a positive integer, got {self.num_channels!r}"
            )

        if self.num_timesteps <= 0:
            raise ValueError(
                f"num_timesteps must be a positive integer, got {self.num_timesteps!r}"
            )


@dataclass(slots=True)
class Observation:
    """Observation configuration and derived sampling grids."""

    start_time: float
    observation_length: float
    num_timesteps: int
    start_frequency: float
    num_channels: int
    total_bandwidth: float
    spec: "ObservationSpec | None" = None

    # Lazy cached arrays
    _times: np.ndarray | None = field(default=None, init=False, repr=False)
    _frequencies: np.ndarray | None = field(default=None, init=False, repr=False)

    @classmethod
    def from_spec(cls, spec: "ObservationSpec") -> "Observation":
        """Create an Observation instance from an ObservationSpec."""
        return cls(
            start_time=spec.start_time,
            observation_length=spec.observation_length,
            num_timesteps=spec.num_timesteps,
            start_frequency=spec.start_frequency,
            num_channels=spec.num_channels,
            total_bandwidth=spec.total_bandwidth,
            spec=spec,
        )

    @property
    def channel_width(self) -> float:
        """Return the width of each frequency channel."""
        return self.total_bandwidth / self.num_channels

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
