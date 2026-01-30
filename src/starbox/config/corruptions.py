"""Corruptions configuration schema."""

from pydantic import BaseModel, Field


class CorruptionsConfig(BaseModel):
    seed: int = Field(ge=0)
    rms_noise: float = Field(ge=0)
    rms_phase_gain: float = Field(ge=0)
