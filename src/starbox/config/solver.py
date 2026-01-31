"""Solver configuration schema."""

from pydantic import BaseModel, Field


class SolverConfig(BaseModel):
    """Configuration schema for the solver."""

    solution_interval_seconds: float = Field(
        gt=0, description="Solution interval in seconds."
    )
