"""Experiment configuration schema."""

from pydantic import BaseModel, Field

from starbox.config import (
    SkyModelConfig,
    ObservationConfig,
    CorruptionsConfig,
    SolverConfig,
    TelescopeConfig,
)


class ExperimentConfig(BaseModel):
    """Configuration for a simulation experiment."""

    name: str = Field(..., description="Name of the experiment.")
    description: str | None = Field(
        None, description="Optional description of the experiment."
    )
    telescope: TelescopeConfig = Field(
        ..., description="Configuration for the telescope array."
    )
    skymodel: SkyModelConfig = Field(
        ..., description="Configuration for the sky model."
    )
    observation: ObservationConfig = Field(
        ..., description="Configuration for the observation."
    )
    corruptions: CorruptionsConfig = Field(
        ..., description="Configuration for the corruptions to apply."
    )
    solver: SolverConfig = Field(
        ..., description="Configuration for the calibration solver."
    )
