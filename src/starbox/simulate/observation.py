"""Class for handling observation parameters."""


class Observation:
    def __init__(
        self,
        start_time,
        observation_length,
        num_timesteps,
        start_frequency,
        num_channels,
        total_bandwidth,
    ):
        self.start_time = start_time
        self.observation_length = observation_length
        self.num_timesteps = num_timesteps
        self.start_frequency = start_frequency
        self.num_channels = num_channels
        self.total_bandwidth = total_bandwidth
        self.channel_width = total_bandwidth / num_channels

    @property
    def times(self):
        """Generate an array of time steps for the observation."""
        return [
            self.start_time + i * (self.observation_length / self.num_timesteps)
            for i in range(self.num_timesteps)
        ]

    @property
    def frequencies(self):
        """Generate an array of frequency channels for the observation."""
        return [
            self.start_frequency + i * self.channel_width
            for i in range(self.num_channels)
        ]
