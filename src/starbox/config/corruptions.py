"""Corruptions configuration schema."""

from pydantic import BaseModel, Field


class CorruptionsConfig(BaseModel):
    """Configuration schema for the Corruptions."""

    seed: int = Field(ge=0)
    rms_noise: float = Field(ge=0)
    rms_phase_gain: float = Field(ge=0)
    phase_time_correlation: float = Field(default=0.95, ge=0.0, lt=1.0)
    phase_frequency_correlation: float = Field(default=0.85, ge=0.0, lt=1.0)
