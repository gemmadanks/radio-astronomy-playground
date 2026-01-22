"""Starbox: A Python package for exploring radio astronomy concepts.

This package provides tools and simulations for radio astronomy concepts,
including telescope array configuration and sky models.

Modules:
    simulate: Radio telescope simulation components including the Telescope class
              for modeling antenna arrays and their configurations and SkyModel for
              simulating sky models.
"""

from .simulate import Telescope, SkyModel, Observation
from .simulate.corruptions import Corruptions
from .image.imager import Imager
from .calibrate.solver import Solver


__version__ = "0.4.0"
__all__ = ["Telescope", "SkyModel", "Corruptions", "Imager", "Solver", "Observation"]
