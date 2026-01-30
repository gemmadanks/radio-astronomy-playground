"""Module for configuration schemas."""

from .observation import ObservationConfig
from .skymodel import SkyModelConfig
from .telescope import TelescopeConfig
from .corruptions import CorruptionsConfig
from .solver import SolverConfig

__all__ = [
    "ObservationConfig",
    "SkyModelConfig",
    "TelescopeConfig",
    "CorruptionsConfig",
    "SolverConfig",
]
