"""A class for simulating sky models."""

import numpy as np
from dataclasses import dataclass


@dataclass(slots=True)
class SkyModelSpec:
    """A dataclass representing the specification for a sky model.

    Attributes:
        num_sources: Number of sources to generate
        max_flux_jy: Maximum flux density in Jy
        phase_centre_deg: (RA, Dec) coordinates in degrees
        fov_deg: Field of view in degrees
        seed: Random seed for reproducibility
    """

    num_sources: int = 1
    max_flux_jy: float = 1.0
    phase_centre_deg: tuple[float, float] = (0, 0)
    fov_deg: float = 1.0
    seed: int = 42

    def __post_init__(self):
        if self.num_sources <= 0:
            raise ValueError(f"num_sources must be > 0, got {self.num_sources!r}")
        if self.max_flux_jy <= 0:
            raise ValueError(f"max_flux_jy must be > 0, got {self.max_flux_jy!r}")
        if self.fov_deg <= 0:
            raise ValueError(f"fov_deg must be > 0, got {self.fov_deg!r}")


@dataclass(slots=True)
class SkyModel:
    name: str
    ra_deg: np.ndarray
    dec_deg: np.ndarray
    flux_jy: np.ndarray
    spec: "SkyModelSpec | None" = None

    @classmethod
    def from_spec(cls, spec: "SkyModelSpec", name: str = "Sky Model") -> "SkyModel":
        rng = np.random.default_rng(spec.seed)

        ra_centre, dec_centre = spec.phase_centre_deg
        half_fov_deg = spec.fov_deg / 2.0

        ra = rng.uniform(
            ra_centre - half_fov_deg, ra_centre + half_fov_deg, spec.num_sources
        )
        dec = rng.uniform(
            dec_centre - half_fov_deg, dec_centre + half_fov_deg, spec.num_sources
        )
        flux = rng.uniform(0.0, spec.max_flux_jy, spec.num_sources)

        return cls(
            name=name,
            ra_deg=ra,
            dec_deg=dec,
            flux_jy=flux,
            spec=spec,
        )

    def __post_init__(self):
        if not (self.ra_deg.shape == self.dec_deg.shape == self.flux_jy.shape):
            raise ValueError("ra_deg, dec_deg, flux_jy must have same shape")

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
