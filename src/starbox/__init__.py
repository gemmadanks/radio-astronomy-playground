"""Starbox: A Python package for exploring radio astronomy concepts.

This package provides tools and simulations for radio astronomy concepts,
including telescope array configuration and sky models.

Modules:
    simulate: Radio telescope simulation components including the Telescope class
              for modeling antenna arrays and their configurations and SkyModel for
              simulating sky models.
"""

from .simulate import Telescope, SkyModel

__version__ = "0.0.0"
__all__ = ["Telescope", "SkyModel"]
