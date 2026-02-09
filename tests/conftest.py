"""Fixtures for tests."""

import pytest
from starbox.calibrate.solutions import Solutions
from starbox.config.telescope import TelescopeConfig, TelescopeSiteConfig
from starbox.simulate.corruptions import Corruptions
from starbox.simulate.telescope import Telescope
from starbox.simulate.skymodel import SkyModel
from starbox.simulate.observation import Observation
from starbox.config.skymodel import SkyModelConfig
from starbox.config.observation import ObservationConfig
from starbox.config.corruptions import CorruptionsConfig
from starbox.config.solver import SolverConfig
from starbox.visibility import VisibilitySet
import numpy as np
from starbox.config.experiment import ExperimentConfig


@pytest.fixture
def telescope_site_config():
    """A simple telescope site configuration."""
    return TelescopeSiteConfig(latitude_deg=45.0, longitude_deg=90.0, altitude_m=100.0)


@pytest.fixture
def telescope_config(telescope_site_config):
    """A simple telescope configuration."""
    return TelescopeConfig(
        num_stations=10, diameter=20.0, seed=42, site=telescope_site_config
    )


@pytest.fixture
def small_telescope(telescope_config, telescope_site_config):
    """A simple telescope model for a small array."""
    telescope_config.site = telescope_site_config
    return Telescope(telescope_config, name="SmallArray")


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
def skymodel(skymodel_config):
    """A simple sky model instance."""
    return SkyModel(skymodel_config)


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
def observation(observation_config):
    """A simple observation setup."""
    return Observation(observation_config)


@pytest.fixture
def corruptions_config():
    """A simple corruptions configuration."""
    return CorruptionsConfig(
        seed=42,
        rms_noise=1.0,
        rms_phase_gain=2.0,
    )


@pytest.fixture
def corruptions(corruptions_config):
    """A simple Corruptions instance."""
    return Corruptions(corruptions_config)


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
def solver_config():
    """A simple solver configuration."""
    return SolverConfig(solution_interval_seconds=10)


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
