"""Telescope configuration schema."""

from pydantic import BaseModel, Field


class TelescopeSiteConfig(BaseModel):
    """Configuration schema for the Telescope site."""

    latitude_deg: float = Field(ge=-90.0, le=90.0)
    longitude_deg: float = Field(ge=-180.0, le=180.0)
    altitude_m: float


class TelescopeConfig(BaseModel):
    """Configuration schema for the Telescope."""

    num_stations: int = Field(gt=0)
    diameter: float = Field(gt=0)
    seed: int = Field(ge=0)
    site: TelescopeSiteConfig
