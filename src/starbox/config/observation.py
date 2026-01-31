"""Observation configuration schema."""

from pydantic import BaseModel, Field


class ObservationConfig(BaseModel):
    """Configuration schema for the Observation."""

    start_time: float = Field(ge=0)
    observation_length: float = Field(gt=0)
    num_timesteps: int = Field(ge=1)
    start_frequency: float = Field(gt=0)
    num_channels: int = Field(ge=1)
    total_bandwidth: float = Field(gt=0)
