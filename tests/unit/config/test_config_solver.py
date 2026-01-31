"""Tests for solver configuration."""

from starbox.config.solver import SolverConfig
import pytest
from pydantic import ValidationError


def test_solver_config_from_dict():
    parameter_dict = {
        "solution_interval_seconds": 10,
    }
    solver_config = SolverConfig(**parameter_dict)
    for key, value in parameter_dict.items():
        assert getattr(solver_config, key) == value


def test_solver_config_valid():
    cfg = SolverConfig(solution_interval_seconds=10)
    assert cfg.solution_interval_seconds == 10


def test_solver_config_rejects_bad_solution_interval_seconds():
    with pytest.raises(ValidationError):
        SolverConfig(solution_interval_seconds=0)
    with pytest.raises(ValidationError):
        SolverConfig(solution_interval_seconds=-5)


def test_solver_config_roundtrip_json():
    cfg = SolverConfig(solution_interval_seconds=10)
    cfg2 = SolverConfig.model_validate_json(cfg.model_dump_json())
    assert cfg2 == cfg
