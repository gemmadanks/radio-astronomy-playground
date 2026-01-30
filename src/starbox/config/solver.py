"""Solver configuration schema."""

from pydantic import BaseModel, Field


class SolverConfig(BaseModel):
    """Configuration for the solver."""

    solint: float = Field(gt=0, description="Solution interval in seconds.")
