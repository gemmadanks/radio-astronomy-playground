"""A class for simulating sky models."""

import numpy as np

from starbox.config.skymodel import SkyModelConfig
import plotly.express as px

class SkyModel:
    """A class representing a sky model.

    Attributes:
        name: The name of the sky model.
        ra_deg: Right ascension of sources in degrees.
        dec_deg: Declination of sources in degrees.
        flux_jy: Flux densities of sources in Jansky.
        config: The SkyModelConfig used to generate this sky model.
    """

    def __init__(
        self,
        config: SkyModelConfig,
        name: str = "Sky Model",
    ):
        self.name = name
        self.config = config
        self._generate_sources()

    def _generate_sources(self):
        """Generate the sky model sources."""
        rng = np.random.default_rng(self.config.seed)
        ra_centre, dec_centre = self.config.phase_centre_deg
        half_fov_deg = self.config.fov_deg / 2.0

        self.ra_deg = rng.uniform(
            ra_centre - half_fov_deg, ra_centre + half_fov_deg, self.config.num_sources
        )
        self.dec_deg = rng.uniform(
            dec_centre - half_fov_deg,
            dec_centre + half_fov_deg,
            self.config.num_sources,
        )
        self.flux_jy = rng.uniform(
            0.0, self.config.max_flux_jy, self.config.num_sources
        )

    def as_arrays(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return self.ra_deg, self.dec_deg, self.flux_jy

    def equals(self, other: "SkyModel", atol: float = 0.0, rtol: float = 0.0) -> bool:
        """Check equality with another SkyModel within a tolerance."""
        ra1, dec1, f1 = self.as_arrays()
        ra2, dec2, f2 = other.as_arrays()

        return (
            np.allclose(ra1, ra2, atol=atol, rtol=rtol)
            and np.allclose(dec1, dec2, atol=atol, rtol=rtol)
            and np.allclose(f1, f2, atol=atol, rtol=rtol)
        )
