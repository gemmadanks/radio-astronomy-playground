"""Solver configuration schema."""

from pydantic import BaseModel, Field


class SolverConfig(BaseModel):
    """Configuration schema for the solver."""

    solution_interval_seconds: float = Field(
        gt=0, description="Solution interval in seconds."
    )
    solution_interval_hz: float | None = Field(
        default=None,
        gt=0,
        description="Optional solution interval in Hz. If omitted, solve per channel.",
    )
