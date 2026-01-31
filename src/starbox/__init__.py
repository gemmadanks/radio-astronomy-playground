"""Starbox: A Python package for exploring radio astronomy concepts.

This package provides tools and simulations for radio astronomy concepts,
including telescope array configuration and sky models.

Modules:
    simulate: Radio telescope simulation components including the Telescope class
              for modeling antenna arrays and their configurations, SkyModel for
              simulating sky models, and Observation for observation setups.
    config: Configuration classes for various simulation components.
    factory: Factory functions to build simulation components from configurations.
    calibrate: Calibration tools including Solver for gain calibration.
    image: Imaging tools including Imager for creating images from visibilities.
    predict: Functions to predict visibilities from sky models and telescope configurations.
    io: Input/output utilities for saving and loading simulation data.
"""

from .simulate import Telescope, SkyModel, Observation
from .config import (
    TelescopeConfig,
    SkyModelConfig,
    ObservationConfig,
    CorruptionsConfig,
    SolverConfig,
)
from .simulate.corruptions import Corruptions
from .factory import (
    build_telescope,
    build_skymodel,
    build_observation,
    build_corruptions,
    build_solver,
)
from .image.imager import Imager
from .calibrate.solver import Solver
from .predict import predict_visibilities
from .io import save


__version__ = "0.6.3"
__all__ = [
    "Telescope",
    "SkyModel",
    "Corruptions",
    "Imager",
    "Solver",
    "predict_visibilities",
    "build_telescope",
    "build_skymodel",
    "build_observation",
    "build_corruptions",
    "build_solver",
    "save",
    "Observation",
    "TelescopeConfig",
    "SkyModelConfig",
    "ObservationConfig",
    "CorruptionsConfig",
    "SolverConfig",
]
