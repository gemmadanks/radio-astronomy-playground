"""Sky model configuration schema."""

from pydantic import BaseModel, Field


class SkyModelConfig(BaseModel):
    """Configuration schema for the SkyModel."""

    num_sources: int = Field(gt=0)
    max_flux_jy: float = Field(gt=0)
    phase_centre_deg: tuple[float, float] = Field(default=(0, 0))
    fov_deg: float = Field(gt=0)
    seed: int = Field(ge=0)
