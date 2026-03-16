"""Telescope class.

This module contains the Telescope class.

Example:
    >>> from starbox.simulate import Telescope
    >>> from starbox.config import TelescopeConfig, TelescopeSiteConfig
    >>> site_config = TelescopeSiteConfig(latitude_deg=45.0, longitude_deg=90.0, altitude_m=100.0)
    >>> config = TelescopeConfig(num_stations=100, diameter=50.0, seed=42, site=site_config)
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
        self.num_stations = self.config.num_stations
        self.num_baselines = self.num_stations * (self.num_stations - 1) // 2
        self.station_positions = self._configure_array()
        self.station_ids = np.array(
            [f"{self.name}_STN{idx:03d}" for idx in range(self.num_stations)]
        )
        self.baselines_ecef = self._compute_baselines(self._enu_to_ecef())

    def _configure_array(self) -> np.ndarray:
        """Configure an array of antennas.

        Generates a numpy array of shape (num_stations, 3) representing antenna positions in east,
        north, and up arranged randomly within a circle of the telescope's diameter.
        """
        angles = self._get_angles()
        radii = self._get_radii()
        east, north, up = _compute_enu_coordinates(angles, radii)
        return np.column_stack((east, north, up))

    def _compute_baselines(self, positions) -> np.ndarray:
        """Compute baselines from station positions.

        Args:
            positions: A numpy array of shape (num_stations, 3) containing the coordinates of each station.

        Returns:
            A numpy array of shape (num_baselines, 3) containing the baseline vectors.
        """
        i, j = np.triu_indices(self.num_stations, k=1)
        return positions[j] - positions[i]

    def _get_angles(self) -> np.ndarray:
        """Generate random angles for antenna placement."""
        return self.rng.uniform(0, 2 * np.pi, self.num_stations)

    def _get_radii(self) -> np.ndarray:
        """Generate random radii for antenna placement within the telescope diameter."""
        radius = self.config.diameter / 2
        return radius * np.sqrt(self.rng.uniform(0, 1, self.num_stations))

    def _enu_to_ecef(self) -> np.ndarray:
        """Express station ENU offsets in the ECEF basis at the telescope site.

        This method uses the telescope's station positions stored in
        ``self.station_positions`` (in local ENU coordinates) and applies the
        site-specific ENU→ECEF rotation matrix. The result is a set of station
        displacement vectors expressed in the global Earth-Centered, Earth-Fixed
        (ECEF) coordinate basis, but **no origin translation to the site's
        absolute ECEF position is applied**.

        This is appropriate for computing baselines (differences between station
        vectors), where any common origin offset cancels out. It does *not*
        produce absolute ECEF positions of the stations.

        Returns:
            A numpy array of shape (num_stations, 3) containing station vectors
            in the ECEF basis at the site.
        """
        rotation_matrix = self._rotation_matrix()
        ecef = self.station_positions @ rotation_matrix.T
        return ecef

    def _rotation_matrix(self) -> np.ndarray:
        """Calculate the ENU→ECEF rotation matrix at the telescope site.

        The returned matrix rotates local ENU vectors at the site's latitude and
        longitude into the global Earth-Centered, Earth-Fixed (ECEF) frame.
        """
        lat0_rad = np.radians(self.config.site.latitude_deg)
        lon0_rad = np.radians(self.config.site.longitude_deg)

        return np.array(
            [
                [
                    -np.sin(lon0_rad),
                    -np.sin(lat0_rad) * np.cos(lon0_rad),
                    np.cos(lat0_rad) * np.cos(lon0_rad),
                ],
                [
                    np.cos(lon0_rad),
                    -np.sin(lat0_rad) * np.sin(lon0_rad),
                    np.cos(lat0_rad) * np.sin(lon0_rad),
                ],
                [0, np.cos(lat0_rad), np.sin(lat0_rad)],
            ]
        )


def _compute_enu_coordinates(
    angles: np.ndarray, radii: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate ENU coordinates from angles and radii.

    Args:
        angles: Array of angles in radians for each station.
        radii: Array of radii for each station.

    Returns:
        Tuple of (east, north, up) coordinates for each station.
    """
    east = radii * np.sin(angles)
    north = radii * np.cos(angles)
    up = np.zeros(len(angles))
    return east, north, up
