"""Fixtures for tests."""

import pytest
from starbox.simulate.telescope import Telescope
import plotly.io as pio
from starbox.simulate.skymodel import SkyModel
from starbox.simulate.observation import Observation


@pytest.fixture(scope="session", autouse=True)
def configure_plotly_for_tests():
    """Configure Plotly to not open browser during tests."""
    # Set renderer to 'json' or 'png' instead of 'browser'
    pio.renderers.default = "json"


@pytest.fixture
def small_telescope():
    """A simple telescope model for a small array."""
    return Telescope(name="SmallArray", num_stations=10, diameter=20.0)


@pytest.fixture
def skymodel():
    """A simple sky model with a few sources."""
    return SkyModel(name="SmallSkyModel", num_sources=5, seed=42)


@pytest.fixture
def observation():
    """A simple observation setup."""
    start_time = 0  # in seconds
    observation_length = 180  # in seconds
    num_timesteps = 3
    start_frequency = 1e6  # in Hz
    num_channels = 2
    total_bandwidth = 1e6  # in Hz

    return Observation(
        start_time=start_time,
        observation_length=observation_length,
        num_timesteps=num_timesteps,
        start_frequency=start_frequency,
        num_channels=num_channels,
        total_bandwidth=total_bandwidth,
    )
