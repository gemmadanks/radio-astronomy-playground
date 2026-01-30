"""Telescope configuration schema."""

from pydantic import BaseModel, Field


class TelescopeConfig(BaseModel):
    num_stations: int = Field(gt=0)
    diameter: float = Field(gt=0)
    seed: int = Field(ge=0)
