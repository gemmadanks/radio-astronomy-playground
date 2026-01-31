"""Telescope class.

This module contains the Telescope class.

Example:
    >>> from starbox.simulate import Telescope
    >>> from starbox.config import TelescopeConfig
    >>> config = TelescopeConfig(num_stations=100, diameter=50.0, seed=42)
    >>> telescope = Telescope(config, name="ELA")
    >>> print(telescope.name)
    ELA
"""

from starbox.config import TelescopeConfig
import numpy as np


class Telescope:
    """A class representing a radio telescope array."""

    def __init__(
        self,
        cfg: TelescopeConfig,
        name: str = "Telescope",
    ):
        """Initialize the Telescope.

        Args:
            cfg: TelescopeConfig instance containing configuration parameters.
            name: Name of the telescope.
        """
        self.name = name
        self.config = cfg

        self.rng = np.random.default_rng(self.config.seed)
        self.station_positions = self._configure_array()
        self.station_ids = np.array(
            [f"{self.name}_STN{idx:03d}" for idx in range(self.config.num_stations)]
        )

    def _configure_array(self) -> np.ndarray:
        """Configure an array of antennas.

        Generates a numpy array of shape (num_stations, 3) representing antenna positions in x (north),
        y (east), and z (up) arranged randomly within a circle of the telescope's diameter.
        """
        angles = self._get_angles()
        radii = self._get_radii()
        x, y, z = _compute_coordinates(angles, radii)
        return np.column_stack((x, y, z))

    def _get_angles(self) -> np.ndarray:
        """Generate random angles for antenna placement."""
        return self.rng.uniform(0, 2 * np.pi, self.config.num_stations)

    def _get_radii(self) -> np.ndarray:
        """Generate random radii for antenna placement within the telescope diameter."""
        radius = self.config.diameter / 2
        return radius * np.sqrt(self.rng.uniform(0, 1, self.config.num_stations))


def _compute_coordinates(
    angles: np.ndarray, radii: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate x, y, z coordinates from angles and radii."""
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    z = np.zeros(len(angles))
    return x, y, z
