"""Radio telescope simulation components.

This module provides classes and functions for simulating random radio
telescope array configurations and sky models.

Classes:
    Telescope: A class representing a radio telescope array with random
                antenna configurations.
    SkyModel: A class for simulating sky models with random sources.

Functions:
    _compute_coordinates: Helper function to calculate antenna coordinates from
                         polar coordinates.
"""

from .telescope import Telescope
from .skymodel import SkyModel

__all__ = ["Telescope", "SkyModel"]
