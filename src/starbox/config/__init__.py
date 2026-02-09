"""Module for configuration schemas.

Exports:
    - ObservationConfig: Configuration schema for observations.
    - SkyModelConfig: Configuration schema for sky models.
    - TelescopeConfig: Configuration schema for telescopes.
    - TelescopeSiteConfig: Configuration schema for telescope sites.
    - CorruptionsConfig: Configuration schema for corruptions.
    - SolverConfig: Configuration schema for solvers.
    - ExperimentConfig: Configuration schema for experiments.
"""

from .observation import ObservationConfig
from .skymodel import SkyModelConfig
from .telescope import TelescopeConfig, TelescopeSiteConfig
from .corruptions import CorruptionsConfig
from .solver import SolverConfig
from .experiment import ExperimentConfig

__all__ = [
    "ObservationConfig",
    "SkyModelConfig",
    "TelescopeConfig",
    "TelescopeSiteConfig",
    "CorruptionsConfig",
    "SolverConfig",
    "ExperimentConfig",
]
