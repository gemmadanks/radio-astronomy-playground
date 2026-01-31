"""Functions to build Observation from configuration."""

from starbox.config.observation import ObservationConfig
from starbox.simulate.observation import Observation


def build_observation(config: ObservationConfig) -> Observation:
    """Build an Observation from its configuration.

    Args:
        config: The Observation configuration.
    Returns:
        The built Observation.
    """
    return Observation(config)
