"""Fixtures for tests."""

import pytest
from starbox.calibrate.solutions import Solutions
from starbox.config.telescope import TelescopeConfig
from starbox.simulate.corruptions import Corruptions, CorruptionsSpec
from starbox.simulate.telescope import Telescope, TelescopeSpec
import plotly.io as pio
from starbox.simulate.skymodel import SkyModel, SkyModelSpec
from starbox.simulate.observation import Observation, ObservationSpec
from starbox.config.skymodel import SkyModelConfig
from starbox.config.observation import ObservationConfig
from starbox.config.corruptions import CorruptionsConfig
from starbox.config.solver import SolverConfig
from starbox.visibility import VisibilitySet
import numpy as np
from starbox.calibrate.solver import SolverSpec
from starbox.config.experiment import ExperimentConfig


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
def telescope_spec():
    """A simple TelescopeSpec instance."""
    return TelescopeSpec(num_stations=10, diameter=20.0, seed=42)


@pytest.fixture
def telescope_config():
    """A simple telescope configuration."""
    return TelescopeConfig(num_stations=10, diameter=20.0, seed=42)


@pytest.fixture
def skymodel_spec():
    """A simple sky model with a few sources."""
    return SkyModelSpec(num_sources=5, seed=42)


@pytest.fixture
def skymodel(skymodel_spec):
    """A simple sky model instance."""
    return SkyModel.from_spec(skymodel_spec)


@pytest.fixture
def skymodel_config():
    """A simple sky model configuration."""
    return SkyModelConfig(
        num_sources=5,
        max_flux_jy=1.0,
        fov_deg=1.0,
        phase_centre_deg=(0.0, 0.0),
        seed=42,
    )


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
def observation_config():
    """A simple observation configuration."""
    return ObservationConfig(
        start_time=0,  # in seconds
        observation_length=180,  # in seconds
        num_timesteps=3,
        start_frequency=1e6,  # in Hz
        num_channels=2,
        total_bandwidth=1e6,  # in Hz
    )


@pytest.fixture
def observation_spec():
    """A simple ObservationSpec instance."""
    return ObservationSpec(
        start_time=0,  # in seconds
        observation_length=180,  # in seconds
        num_timesteps=3,
        start_frequency=1e6,  # in Hz
        num_channels=2,
        total_bandwidth=1e6,  # in Hz
    )


@pytest.fixture
def corruptions_config():
    """A simple corruptions configuration."""
    return CorruptionsConfig(
        seed=42,
        rms_noise=1.0,
        rms_phase_gain=2.0,
    )


@pytest.fixture
def corruptions_spec():
    """A simple CorruptionsSpec instance."""
    return CorruptionsSpec(
        seed=42,
        rms_noise=1.0,
        rms_phase_gain=2.0,
    )


@pytest.fixture
def corruptions_basic(corruptions_spec):
    """A simple Corruptions instance."""
    return Corruptions.from_spec(corruptions_spec)


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
def solver_spec():
    """A simple SolverSpec instance."""
    return SolverSpec(solint=10)


@pytest.fixture
def solver_config():
    """A simple solver configuration."""
    return SolverConfig(solint=10)


@pytest.fixture
def gains():
    """A simple gains array for testing."""
    return np.random.rand(3, 2, 4).astype("complex64")


@pytest.fixture
def solutions(gains):
    """A simple Solutions instance for testing."""
    return Solutions(station_phase_gains=gains)


@pytest.fixture
def rng():
    """A random number generator with a fixed seed for reproducibility."""
    return np.random.default_rng(seed=42)


@pytest.fixture
def experiment_config(
    telescope_config,
    skymodel_config,
    observation_config,
    corruptions_config,
    solver_config,
):
    """A simple experiment configuration."""
    return ExperimentConfig(
        name="Test Experiment",
        description="A simple test experiment configuration.",
        telescope=telescope_config,
        skymodel=skymodel_config,
        observation=observation_config,
        corruptions=corruptions_config,
        solver=solver_config,
    )
