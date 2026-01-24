"""Telescope class.

This module contains the Telescope class.

Example:
    >>> from starbox.simulate import Telescope
    >>> telescope = Telescope(name="ELA", num_stations=100, diameter=50.0)
    >>> print(telescope)
    Telescope(name=ELA, num_stations=100, diameter=50.0 m)
"""

import numpy as np


class Telescope:
    """A class representing a radio telescope array."""

    def __init__(self, name: str, num_stations: int, diameter: float, seed: int = 42):
        """Initialize a Telescope object.

        Args:
            name: Identifier for the telescope.
            num_stations: Number of stations in the telescope.
            diameter: Diameter of the telescope in metres.
            seed: Random seed for reproducibility.
        """
        self.name: str = name
        self.num_stations: int = num_stations
        self.diameter: float = diameter
        self.rng: np.random.Generator = np.random.default_rng(seed)
        self.array: np.ndarray = self._configure_array()
        self.station_ids: np.ndarray = np.array(
            [f"{name}_STN{idx:03d}" for idx in range(num_stations)]
        )

    def __repr__(self):
        return f"Telescope(name={self.name}, num_stations={self.num_stations}, diameter={self.diameter} m)"

    def _configure_array(self) -> np.ndarray:
        """Configure an array of antennas.

        Generates a numpy array of shape (num_stations, 3) representing antenna positions in x (north),
        y (east), and z (up) arranged randomly within a circle of the telescope's diameter.
        """
        angles = self._get_angles()
        radii = self._get_radii()
        x, y, z = _compute_coordinates(angles, radii)
        return np.column_stack((x, y, z))

    def reconfigure(self, seed: int | None = None) -> None:
        """Reconfigure the array with a new random configuration.

        Args:
            seed: Optional new seed for random number generator. If None,
                  uses current RNG state for different configuration.
        """
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.array = self._configure_array()

    def _get_angles(self) -> np.ndarray:
        """Generate random angles for antenna placement."""
        return self.rng.uniform(0, 2 * np.pi, self.num_stations)

    def _get_radii(self) -> np.ndarray:
        """Generate random radii for antenna placement within the telescope diameter."""
        radius = self.diameter / 2
        return radius * np.sqrt(self.rng.uniform(0, 1, self.num_stations))


def _compute_coordinates(
    angles: np.ndarray, radii: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate x, y, z coordinates from angles and radii."""
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    z = np.zeros(len(angles))
    return x, y, z
