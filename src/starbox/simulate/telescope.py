"""Telescope class.

This module contains the Telescope class.

Example:
    >>> from starbox.simulate import Telescope, TelescopeSpec
    >>> spec = TelescopeSpec(num_stations=100, diameter=50.0, seed=42)
    >>> telescope = Telescope.from_spec(spec, name="ELA")
    >>> print(telescope.name)
    ELA
"""

from dataclasses import dataclass
import numpy as np


@dataclass(slots=True)
class TelescopeSpec:
    """A dataclass representing the specification for a telescope.
    Attributes:
        num_stations: Number of stations in the telescope array.
        diameter: Diameter of the telescope in meters.
        seed: Random seed for reproducibility.
    """

    num_stations: int
    diameter: float
    seed: int = 42

    def __post_init__(self):
        if self.num_stations <= 0:
            raise ValueError(f"num_stations must be > 0, got {self.num_stations!r}")
        if self.diameter <= 0:
            raise ValueError(f"diameter must be > 0, got {self.diameter!r}")


@dataclass(slots=True)
class Telescope:
    """A class representing a radio telescope array."""

    name: str
    num_stations: int
    diameter: float
    array: np.ndarray | None = None
    station_ids: np.ndarray | None = None
    seed: int | None = None
    spec: "TelescopeSpec | None" = None

    def __post_init__(self):
        rng = np.random.default_rng(self.seed)
        if self.array is None:
            self.array = self._configure_array(rng)
        if self.station_ids is None:
            self.station_ids = np.array(
                [f"{self.name}_STN{idx:03d}" for idx in range(self.num_stations)]
            )
        if self.array.shape != (self.num_stations, 3):
            raise ValueError(
                f"Array shape must be ({self.num_stations}, 3), got {self.array.shape!r}"
            )
        if self.station_ids.shape != (self.num_stations,):
            raise ValueError(
                f"station_ids shape must be ({self.num_stations},), got {self.station_ids.shape!r}"
            )

    @classmethod
    def from_spec(cls, spec: "TelescopeSpec", name: str = "Telescope") -> "Telescope":
        """Create a Telescope instance from a TelescopeSpec."""
        return cls(
            name=name,
            num_stations=spec.num_stations,
            diameter=spec.diameter,
            station_ids=None,
            spec=spec,
            array=None,
            seed=spec.seed,
        )

    def _configure_array(self, rng: np.random.Generator) -> np.ndarray:
        """Configure an array of antennas.

        Generates a numpy array of shape (num_stations, 3) representing antenna positions in x (north),
        y (east), and z (up) arranged randomly within a circle of the telescope's diameter.
        """
        angles = self._get_angles(rng)
        radii = self._get_radii(rng)
        x, y, z = _compute_coordinates(angles, radii)
        return np.column_stack((x, y, z))

    def _get_angles(self, rng: np.random.Generator) -> np.ndarray:
        """Generate random angles for antenna placement."""
        return rng.uniform(0, 2 * np.pi, self.num_stations)

    def _get_radii(self, rng: np.random.Generator) -> np.ndarray:
        """Generate random radii for antenna placement within the telescope diameter."""
        radius = self.diameter / 2
        return radius * np.sqrt(rng.uniform(0, 1, self.num_stations))


def _compute_coordinates(
    angles: np.ndarray, radii: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate x, y, z coordinates from angles and radii."""
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    z = np.zeros(len(angles))
    return x, y, z
