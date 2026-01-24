"""Fixtures for tests."""

import pytest
from starbox.simulate.corruptions import Corruptions
from starbox.simulate.telescope import Telescope
import plotly.io as pio
from starbox.simulate.skymodel import SkyModel
from starbox.simulate.observation import Observation

from starbox.visibility import VisibilitySet
import numpy as np


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


@pytest.fixture
def corruptions():
    """A simple Corruptions instance."""
    return Corruptions()


@pytest.fixture
def visibility_set():
    """A simple VisibilitySet instance."""

    num_times = 3
    num_baselines = 2
    num_channels = 2

    vis = np.ones((num_times, num_baselines, num_channels), dtype=np.complex128)
    uvw_m = np.zeros((num_times, num_baselines, 3))
    station1 = np.array([0, 1])
    station2 = np.array([1, 2])
    times_mjd = np.array([59000.0, 59000.00069444, 59000.00138889])  # Example MJDs
    freqs_hz = np.array([1e6, 1.5e6])
    weights = np.ones((num_times, num_baselines, num_channels))

    return VisibilitySet(
        vis=vis,
        uvw_m=uvw_m,
        station1=station1,
        station2=station2,
        times_mjd=times_mjd,
        freqs_hz=freqs_hz,
        weights=weights,
    )


@pytest.fixture
def gains():
    """A simple gains array for testing."""
    return np.random.rand(3, 2, 4).astype("complex64")
