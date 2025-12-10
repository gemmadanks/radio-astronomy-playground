"""A class for simulating sky models."""

import numpy as np
import plotly.express as px
from plotly.graph_objects import Figure


class SkyModel:
    """A class representing a sky model for radio astronomy simulations."""

    def __init__(
        self,
        name: str,
        num_sources: int,
        max_flux: float = 1.0,
        phase_centre: tuple[float, float] = (0, 0),
        fov: float = 1.0,
        seed: int = 42,
    ):
        """Initialize a SkyModel object.

        Args:
            name: Identifier for the sky model
            num_sources: Number of sources to generate (must be > 0)
            max_flux: Maximum flux density in Jy (must be >= 0)
            phase_centre: (RA, Dec) coordinates in degrees
            fov: Field of view in degrees (must be > 0)
            seed: Random seed for reproducibility
        """
        self.name = name
        self.num_sources = num_sources
        self.max_flux = max_flux
        self.phase_centre = phase_centre
        self.fov = fov
        self.rng = np.random.default_rng(seed)
        self.sources: list[tuple[tuple[float, float], float]] = []
        self._generate()

    def __repr__(self):
        return f"SkyModel(num_sources={self.num_sources}, max_flux={self.max_flux}, phase_centre={self.phase_centre}, fov={self.fov})"

    def plot(self, show: bool = True) -> Figure:
        """Plot the sky model sources."""
        ras, decs, fluxes = zip(
            *[(pos[0], pos[1], flux) for (pos, flux) in self.sources]
        )
        fig = px.scatter(
            x=ras,
            y=decs,
            size=fluxes,
            title="Sky Model",
            labels={"x": "Right Ascension (deg)", "y": "Declination (deg)"},
        )
        fig.update_yaxes(scaleanchor="x", scaleratio=1)
        if show:
            fig.show()
        return fig

    def regenerate(self, seed: int | None = None):
        """Generate new random sources within the field of view."""
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self._generate()

    def _generate(self):
        """Generate random sources within the field of view."""
        ras = self._get_ra_positions()
        decs = self._get_dec_positions()
        fluxes = self._get_source_fluxes()
        self.sources = list(zip(zip(ras, decs), fluxes))

    def _get_ra_positions(self) -> np.ndarray:
        return self._get_coordinate_positions(self.phase_centre[0])

    def _get_dec_positions(self) -> np.ndarray:
        return self._get_coordinate_positions(self.phase_centre[1])

    def _get_coordinate_positions(self, centre: float) -> np.ndarray:
        """Return the positions of the sources."""
        return self.rng.uniform(
            centre - self.fov / 2, centre + self.fov / 2, self.num_sources
        )

    def _get_source_fluxes(self) -> np.ndarray:
        """Return the fluxes of the sources."""
        return self.rng.uniform(0, self.max_flux, self.num_sources)
