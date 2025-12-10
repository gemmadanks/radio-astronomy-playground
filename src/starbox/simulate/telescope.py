"""Telescope class.

This module contains the Telescope class.

Example:
    >>> from starbox.simulate import Telescope
    >>> telescope = Telescope(name="ELA", num_antennas=100, diameter=50.0)
    >>> print(telescope)
    Telescope(name=ELA, num_antennas=100, diameter=50.0)
"""

import numpy as np
import plotly.express as px
from plotly.graph_objects import Figure


class Telescope:
    """A class representing a radio telescope array."""

    def __init__(self, name: str, num_antennas: int, diameter: float, seed: int = 42):
        """Initialize a Telescope object.

        Args:
            name: Identifier for the telescope.
            num_antennas: Number of antennas in the telescope.
            diameter: Diameter of the telescope in metres.
            seed: Random seed for reproducibility.
        """
        self.name = name
        self.num_antennas = num_antennas
        self.diameter = diameter
        self.rng = np.random.default_rng(seed)
        self.array: np.ndarray = self._configure_array()

    def __repr__(self):
        return f"Telescope(name={self.name}, num_antennas={self.num_antennas}, diameter={self.diameter})"

    def _configure_array(self) -> np.ndarray:
        """Configure an array of antennas.

        Generates a numpy array of shape (num_antennas, 3) representing antenna positions in x (north),
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

    def plot(self, show: bool = True) -> Figure:
        """Plot the telescope array configuration."""

        fig = px.scatter(
            x=self.array[:, 0],
            y=self.array[:, 1],
            title=f"Telescope Array Configuration: {self.name}",
        )
        fig.update_layout(
            xaxis_title="X (North) [m]",
            yaxis_title="Y (East) [m]",
            yaxis_scaleanchor="x",
            yaxis_scaleratio=1,
        )
        fig.update_traces(marker=dict(size=15, color="blue", symbol="cross"))
        if show:
            fig.show()
        return fig

    def _get_angles(self) -> np.ndarray:
        """Generate random angles for antenna placement."""
        return self.rng.uniform(0, 2 * np.pi, self.num_antennas)

    def _get_radii(self) -> np.ndarray:
        """Generate random radii for antenna placement within the telescope diameter."""
        radius = self.diameter / 2
        return radius * np.sqrt(self.rng.uniform(0, 1, self.num_antennas))


def _compute_coordinates(angles, radii) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate x, y, z coordinates from angles and radii."""
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    z = np.zeros(len(angles))
    return x, y, z
